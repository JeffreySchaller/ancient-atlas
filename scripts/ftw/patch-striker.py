#!/usr/bin/env python3
"""
patch-striker.py - Feel the Weight : in-frame controls + high-striker push
=========================================================================
2026-08-09

WHY
---
Two complaints, one root cause. Nothing told you the block could be spun,
and nothing told you what "try to lift" was for. Every instruction lived
OUTSIDE the frame, so the frame read as a picture rather than a control.

WHAT CHANGES
------------
1. Everything interactive moves ONTO the stage with the rock:
   - a control cluster of physical buttons  (SPIN / RESET / CINEMA)
   - a carnival high-striker gauge down the right edge
   - a persistent instruction chip, bottom left
   - the PUSH button, bottom right
   Finger-drag on mobile and mouse-drag on desktop are untouched.

2. The mechanic changes from LIFT to PUSH. Nobody ever lifted these
   stones; crews dragged them on sledges. So the striker's bell is set at
   breakaway friction, not weight:

       F_breakaway = MU * W,  MU = 0.25

   0.25 is the wetted-sand sledge figure and it is deliberately the
   FRIENDLIEST honest number in the literature - dry sand is roughly
   double, and the Djehutihotep relief shows a man pouring water in front
   of the sledge for exactly this reason. Using the generous coefficient
   matters: the stones still win by four orders of magnitude, and nobody
   can say the demo stacked the deck.

3. Motion is scaled honestly. Below breakaway you get pre-slip creep -
   real, documented, and going nowhere. It scales as ratio^0.6, so the
   2.5-ton Giza block visibly shifts a few centimetres at full effort and
   the 1,500-ton Forgotten Stone does not move a hair. Nothing ever
   breaks away, because nothing ever would.

4. CINEMA mode drops the camera to eye height, close in, on a wide lens,
   and walks the scale figure into the foreground - the car-advert angle,
   which does here what it does there: you stop looking AT the object and
   start standing next to it. Standoff keys off block HEIGHT, not framing
   width, so the 57 m Trilithon puts you at the wall rather than in the
   next field.

The lift-based crew numbers on the seven shipped OG cards stay TRUE - the
verdict now reports both the push crew and the lift crew.

Idempotent. Run from this directory, then patch-inject.py.
"""
import re
import sys
from pathlib import Path

APP = Path(__file__).parent / "app.html"

edits = []          # (label, old, new)
inserts = []        # (label, anchor_substring, block, after_offset)


def E(label, old, new):
    edits.append((label, old, new))


# ---------------------------------------------------------------- copy
E("title",
  "<title>Feel the Weight — try to lift it · The Ancient Atlas</title>",
  "<title>Feel the Weight — try to move it · The Ancient Atlas</title>")

E("meta description",
  'content="Six ancient stones, from a 2.5-ton Giza block to the 1,500-ton Forgotten Stone. Press and hold to try to lift one. You cannot."',
  'content="Six ancient stones, from a 2.5-ton Giza block to the 1,500-ton Forgotten Stone. Push as hard as you can and watch the striker. Not one of them moves."')

E("og:title",
  'content="Feel the Weight — try to lift it"',
  'content="Feel the Weight — try to move it"')

E("og:description",
  'content="Your whole body pulls about 200 lb. The Forgotten Stone needs 3,307,500. Press and hold."',
  'content="Your whole body pushes about 200 lb. Breaking the Forgotten Stone loose takes 826,875. Hold the striker."')

E("mobile kicker",
  '<i style="width:26px;height:1px;background:rgba(201,168,76,.5)"></i>Hold the button below',
  '<i style="width:26px;height:1px;background:rgba(201,168,76,.5)"></i>Spin it, then hold PUSH')

E("mobile screen label", 'data-screen-label="M02 The lift"', 'data-screen-label="M02 The push"')

E("mobile stage height",
  'style="position:relative;z-index:2;height:42vh;min-height:232px;max-height:362px;margin:2px 0 0;transition:opacity .35s ease"',
  'style="position:relative;z-index:2;height:54vh;min-height:320px;max-height:470px;margin:2px 0 0;transition:opacity .35s ease"')

E("mobile rule copy",
  "No one moves this stone alone.<br />The meter shows how close you get.",
  "No one moves this stone alone.<br />The striker shows how close you get.")

E("desktop rule copy",
  "No single person can move this stone.<br />It has never been done alone.<br />The meter measures how close you get.",
  "No single person can move this stone.<br />It has never been done alone.<br />The striker measures how close you get.")

E("desktop footnote",
  "Hold the button, or hold the space bar. Volume up — you'll hear it land.",
  "Hold PUSH, or hold the space bar. Volume up — you'll hear it settle.")

# ------------------------------------------------------------- physics
E("constants",
  "const RAMP = 2.2, PLATEAU_AT = 1.25, GIVE_AT = 2.15;",
  """const RAMP = 2.2, PLATEAU_AT = 1.25, GIVE_AT = 2.15;

/* ---- the push model -----------------------------------------------------
   The old mechanic asked you to LIFT, which is not a thing anyone ever did
   to these stones. Crews dragged them on sledges. So the striker's bell is
   breakaway friction, not weight: F = MU * W.

   MU = 0.25 is the wetted-sand sledge figure, and it is deliberately the
   friendliest honest number available - dry sand runs roughly double, and
   the Djehutihotep relief shows a man pouring water in front of the sledge
   for precisely this reason. Taking the generous coefficient matters: the
   stones still win by four orders of magnitude, so nobody can argue the
   demo stacked the deck.

   CREEP_P shapes pre-slip displacement. Granular beds do not sit rigid and
   then jump - they creep as you approach breakaway. ratio^0.6 gives the
   2.5-ton block a few visible centimetres at full effort and gives the
   1,500-ton block nothing at all, which is the truth. */
const MU = 0.25, CREEP_P = 0.6, CREEP_M = 0.09;""")

E("state",
  "  state = { k:'giza', bw:180, soundOn:true, phase:'idle', tried:false, peak:0, narrow:null, shared:'' };",
  "  state = { k:'giza', bw:180, soundOn:true, phase:'idle', tried:false, peak:0, narrow:null, shared:'', spinOn:true, cine:false };")

E("force helpers",
  "  pullMax() { return Math.max(60, +this.props.pullMax || 200); }",
  """  pullMax() { return Math.max(60, +this.props.pullMax || 200); }
  /* what it takes to break this stone loose on a sledge, in lb */
  breakaway() { return Math.max(1, Math.round(this.site().lb * MU)); }
  /* people pushing exactly as hard as you just did, all at the same instant */
  pushCrew(peak) { return Math.max(2, Math.ceil(this.breakaway() / Math.max(1, peak || this.pullMax()))); }
  liftCrew(peak) { return Math.max(2, Math.ceil(this.site().lb / Math.max(1, peak || this.pullMax()))); }""")

# --------------------------------------------------------- striker paint
E("striker painter",
  "  _msg(t) { document.querySelectorAll('[data-msg]').forEach(el => { el.textContent = t; }); }",
  """  /* The gauge is linear against breakaway, on purpose. A log scale would
     flatter the heavy stones into looking reachable; linear tells you the
     truth by leaving the tube empty. The 0.9% visual floor is the puck
     itself - it exists, it is sitting on the deck, and the number beside
     it says what the height cannot. */
  _paintStriker(pct) {
    const raw = Math.max(0, Math.min(100, pct));
    const h = raw > 0 ? Math.max(0.9, raw) : 0;
    document.querySelectorAll('[data-striker-fill]').forEach(el => { el.style.height = h + '%'; });
    document.querySelectorAll('[data-striker-num]').forEach(el => { el.textContent = this._pctText(pct); });
    if (raw > (this._best || 0)) {
      this._best = raw;
      document.querySelectorAll('[data-striker-best]').forEach(el => {
        el.style.bottom = Math.max(0.9, raw) + '%'; el.style.opacity = '.9';
      });
    }
    const rung = raw >= 100;
    document.querySelectorAll('[data-bell]').forEach(el => {
      el.style.background = rung
        ? 'radial-gradient(circle at 38% 32%,#fff6e0,#E8B960)'
        : 'radial-gradient(circle at 38% 32%,rgba(58,50,29,.92),rgba(9,9,13,.94))';
      el.style.boxShadow = rung
        ? '0 0 24px rgba(232,185,96,.9)'
        : 'inset 0 1px 0 rgba(255,255,255,.06)';
    });
  }
  _clearStriker() {
    this._best = 0;
    document.querySelectorAll('[data-striker-best]').forEach(el => { el.style.opacity = '0'; });
    this._paintStriker(0);
  }

  /* ---------------- stage controls ---------------- */
  _toggleSpin() { this._click(false); this.setState({ spinOn: !this.state.spinOn }, () => { if (this.state.spinOn) this.touched = false; }); }
  _resetView() {
    this._click(false);
    this.rotY = -0.5; this.rotX = 0; this.velY = 0; this.velX = 0;
    this.zoom = 1; this.touched = false; this._hintOff = false;
  }
  _toggleCine() { this._ac(); this._click(false); this.setState({ cine: !this.state.cine }); }

  _msg(t) { document.querySelectorAll('[data-msg]').forEach(el => { el.textContent = t; }); }""")

# ------------------------------------------------------------ hold loop
E("hold loop",
  """      let y = this.restY, jitter = 0;
      if (this.state.phase === 'holding') {
        const held = (performance.now() - this.holdStart) / 1000;
        const max = this.pullMax();
        let f = max * (1 - Math.exp(-held * RAMP));
        if (held > PLATEAU_AT) f = max * (1 - Math.exp(-PLATEAU_AT * RAMP)) + (max - max * (1 - Math.exp(-PLATEAU_AT * RAMP))) * Math.min(1, (held - PLATEAU_AT) / 0.7);
        if (held > PLATEAU_AT && !reduced) f += Math.sin(held * 34) * 2.6;
        this.force = Math.max(0, Math.min(max, f));
        const pct = (this.force / s.lb) * 100;
        this._paintMeter(pct, pct * this._mag());
        if (!reduced && held > PLATEAU_AT) jitter = (Math.random() - 0.5) * 0.006 * Math.max(s.m[1], 1);
        y = this.restY + (this.force / s.lb) * 0.4 + jitter;
        if (held < 0.55) this._msg('You are pulling with ' + Math.round(this.force) + ' lb…');
        else if (held < PLATEAU_AT) this._msg('Harder — ' + Math.round(this.force) + ' lb. Nothing has moved.');
        else this._msg('You are at your limit: ' + Math.round(this.force) + ' lb against ' + s.lb.toLocaleString() + ' lb.');
        if (held > GIVE_AT) this._endHold(true);
      } else if (this.dropAt) {""",
  """      let y = this.restY, jitter = 0, creep = 0, lean = 0;
      if (this.state.phase === 'holding') {
        const held = (performance.now() - this.holdStart) / 1000;
        const max = this.pullMax();
        let f = max * (1 - Math.exp(-held * RAMP));
        if (held > PLATEAU_AT) f = max * (1 - Math.exp(-PLATEAU_AT * RAMP)) + (max - max * (1 - Math.exp(-PLATEAU_AT * RAMP))) * Math.min(1, (held - PLATEAU_AT) / 0.7);
        if (held > PLATEAU_AT && !reduced) f += Math.sin(held * 34) * 2.6;
        this.force = Math.max(0, Math.min(max, f));
        const need = this.breakaway();
        const ratio = this.force / need;
        const pct = ratio * 100;
        this._paintStriker(pct);
        this._paintMeter(pct, pct * this._mag());
        /* Pre-slip creep, not a slide. Scales with the block so a 1.3 m cube
           and a 19.6 m monolith read at the same visual rate, and dies to
           nothing when the ratio is four orders of magnitude down. */
        const take = Math.pow(Math.min(1, ratio), CREEP_P);
        creep = take * CREEP_M * Math.max(1, s.m[0] * 0.35);
        lean = take * 0.02;
        this._creep = creep;
        if (!reduced && held > PLATEAU_AT) jitter = (Math.random() - 0.5) * 0.004 * Math.max(s.m[1], 1) * Math.min(1, ratio * 6);
        if (held < 0.55) this._msg('You are pushing with ' + Math.round(this.force) + ' lb…');
        else if (held < PLATEAU_AT) this._msg('Harder — ' + Math.round(this.force) + ' lb. Breaking it loose takes ' + need.toLocaleString() + '.');
        else this._msg('Your limit: ' + Math.round(this.force) + ' lb. That is ' + this._pctText(pct) + ' of the ' + need.toLocaleString() + ' lb this stone needs.');
        if (held > GIVE_AT) this._endHold(true);
      } else if (this.dropAt) {""")

E("creep applied to pivot",
  """      this.pivot.position.y = y;
    }""",
  """      this.pivot.position.y = y + jitter;
      this.pivot.position.x = creep;
      this.pivot.rotation.z = s.tilt + lean;
    }""")

# -------------------------------------------------------------- verdict
E("verdict lines",
  """    T('[data-tomb1]', (gaveOut ? 'Your grip gave out at ' : 'You pulled ') + peakN.toLocaleString() + ' lb.');
    T('[data-tomb2]', 'It needed ' + s.lb.toLocaleString() + '.');
    T('[data-tomb3]', 'You were ' + shortLb.toLocaleString() + ' lb short.');
    T('[data-tomb4]', 'The stone did not move.');
    T('[data-tomb5]', 'Alone, it never does.');
    T('[data-crew]', 'It would take ' + crew.toLocaleString() + ' people pulling this hard. No engines. Just more people.');""",
  """    const need = this.breakaway();
    const cm = (this._creep || 0) * 100;
    const crewPush = this.pushCrew(peakN), crewLift = this.liftCrew(peakN);
    T('[data-tomb1]', (gaveOut ? 'Your legs gave out at ' : 'You pushed ') + peakN.toLocaleString() + ' lb.');
    T('[data-tomb2]', 'Breaking it loose takes ' + need.toLocaleString() + '.');
    T('[data-tomb3]', 'You reached ' + this._pctText((peakN / need) * 100) + ' of that.');
    T('[data-tomb4]', cm >= 0.5 ? 'It crept ' + cm.toFixed(1) + ' cm and stopped.' : 'It did not move at all.');
    T('[data-tomb5]', 'Alone, it never does.');
    T('[data-crew]', 'It would take ' + crewPush.toLocaleString() + ' people pushing this hard, at the same instant, just to start it sliding. Lifting it clear of the ground would take ' + crewLift.toLocaleString() + '. No engines. Just more people.');""")

E("striker reset on next stone",
  """      this.setState({ k: nx.k, phase: 'idle', tried: false, peak: 0, shared: '' }, () => {
        this._paintMeter(0, 0);""",
  """      this.setState({ k: nx.k, phase: 'idle', tried: false, peak: 0, shared: '' }, () => {
        this._paintMeter(0, 0); this._clearStriker();""")

E("striker reset on pick",
            """            this.setState({ k: x.k, phase: 'idle', tried: false, peak: 0, shared: '' }, () => {
              this._paintMeter(0, 0);""",
            """            this.setState({ k: x.k, phase: 'idle', tried: false, peak: 0, shared: '' }, () => {
              this._paintMeter(0, 0); this._clearStriker();""")

E("endHold clears strain then repaints",
  "    this.setState({ phase: 'failed', peak }, () => this._paintMeter(0, 0));",
  "    this.setState({ phase: 'failed', peak }, () => { this._paintMeter(0, 0); this._paintStriker(0); });")

# --------------------------------------------------------------- camera
E("camera",
  """    const dd = this.camDist * this.zoom;
    let ox = 0, oy = 0;
    if (this._tiltLive && this._tilt && !reduced) { ox = this._tilt.g * 0.004 * dd * 0.1; oy = -this._tilt.b * 0.003 * dd * 0.1; }
    this.camera.position.set(this.camTarget.x + ox, this.camTarget.y + dd * 0.12 + oy, dd);
    this.camera.lookAt(this.camTarget);
    this._usf(this.figure, this.camera);
    this.renderer.render(this.scene, this.camera);""",
  """    const dd = this.camDist * this.zoom;
    let ox = 0, oy = 0;
    if (this._tiltLive && this._tilt && !reduced) { ox = this._tilt.g * 0.004 * dd * 0.1; oy = -this._tilt.b * 0.003 * dd * 0.1; }

    /* ---- study camera  <->  cinematic camera ----------------------------
       STUDY is the original framing: up and back, whole block in view, the
       scale figure standing beside it. It is a camera for reading an object.

       CINEMA is the car-advert angle - eye height, close in, wide lens,
       swung a third of the way round so the long side recedes - and it does
       the same job here that it does for a car: you stop looking AT the
       block and start standing next to it. The standoff keys off block
       HEIGHT rather than framing width on purpose, so the 57 m Trilithon
       puts you at the wall instead of in the next field.

       Both are lerped through the same smoothstep, so the toggle reads as a
       camera move rather than a cut. */
    const cq = this.state.cine ? 1 : 0;
    if (this._cineT === undefined) this._cineT = cq;
    this._cineT += (cq - this._cineT) * (reduced ? 1 : 0.085);
    if (Math.abs(cq - this._cineT) < 0.0015) this._cineT = cq;
    const c = this._cineT * this._cineT * (3 - 2 * this._cineT);

    const bh = Math.max(0.8, s.m[1]);
    const cDist = Math.max(3.0, bh * 1.75) * (0.72 + 0.28 * this.zoom);
    const cAz = 0.66, cSin = Math.sin(cAz), cCos = Math.cos(cAz);
    const camX = (this.camTarget.x + ox) * (1 - c) + (cSin * cDist) * c;
    const camY = (this.camTarget.y + dd * 0.12 + oy) * (1 - c) + 1.42 * c;
    const camZ = dd * (1 - c) + (cCos * cDist) * c;
    const lookY = this.camTarget.y * (1 - c) + Math.max(bh * 0.56, 1.45) * c;
    const lookX = this.camTarget.x * (1 - c);
    const fov = 40 + 26 * c;
    if (Math.abs(this.camera.fov - fov) > 0.01) { this.camera.fov = fov; this.camera.updateProjectionMatrix(); }
    this.camera.position.set(camX, camY, camZ);
    this.camera.lookAt(lookX, lookY, 0);

    /* In cinema the figure walks in off the plinth and stands between you
       and the block, a little to one side. Without this the Trilithon's
       scale figure is 29 m off frame and the whole point is lost. */
    if (this.figure && this._figHome) {
      const fr = 0.44, lat = 1.7;
      this.figure.position.set(
        this._figHome.x * (1 - c) + (cSin * cDist * fr + cCos * lat) * c,
        0,
        this._figHome.z * (1 - c) + (cCos * cDist * fr - cSin * lat) * c
      );
    }
    this._usf(this.figure, this.camera);
    this.renderer.render(this.scene, this.camera);""")

E("autospin honours the spin lock",
  "        if (this.props.autoSpin !== false && !reduced) this.rotY += this._spinRate(now / 1000) * dt;",
  "        if (this.props.autoSpin !== false && this.state.spinOn !== false && !reduced) this.rotY += this._spinRate(now / 1000) * dt;")

E("figure home",
  """    this.figure.updateMatrixWorld(true);
    this.fbox = new THREE.Box3().setFromObject(this.figure);""",
  """    this.figure.updateMatrixWorld(true);
    this._figHome = this.figure.position.clone();
    this.fbox = new THREE.Box3().setFromObject(this.figure);""")

# ------------------------------------------------------------ renderVals
E("needLabel",
  "      needLabel: 'it needs ' + s.lb.toLocaleString() + ' lb',",
  """      needLabel: 'it needs ' + this.breakaway().toLocaleString() + ' lb',
      strikerTop: this.pushCrew(max).toLocaleString() + ' people',
      strikerNeed: this.breakaway().toLocaleString() + ' lb to budge',
      hintSpin: this.state.narrow === true ? 'Swipe the stone to spin it \\u00b7 pinch to zoom' : 'Drag the stone to spin it \\u00b7 scroll to zoom',
      hintPush: 'Hold PUSH \\u2014 the striker shows how close you get',
      spinBg: this.state.spinOn === false ? 'rgba(9,9,13,.72)' : 'rgba(201,168,76,.18)',
      spinFg: this.state.spinOn === false ? '#8A8779' : '#F3D998',
      spinBorder: this.state.spinOn === false ? 'rgba(201,168,76,.26)' : 'rgba(232,185,96,.62)',
      spinLabel: this.state.spinOn === false ? 'Spin off' : 'Spin on',
      cineBg: this.state.cine ? 'rgba(201,168,76,.18)' : 'rgba(9,9,13,.72)',
      cineFg: this.state.cine ? '#F3D998' : '#8A8779',
      cineBorder: this.state.cine ? 'rgba(232,185,96,.62)' : 'rgba(201,168,76,.26)',
      cineLabel: this.state.cine ? 'Cinema on' : 'Cinema',
      toggleSpin: () => this._toggleSpin(),
      resetView: () => this._resetView(),
      toggleCine: () => this._toggleCine(),
      btnPress: holding ? 'translateY(5px)' : 'translateY(0)',""")

E("btnLabel",
  "      btnLabel: holding ? 'Straining…' : tried ? 'Try again' : 'Hold to lift',",
  "      btnLabel: holding ? 'Pushing…' : tried ? 'Push again' : 'Hold to push',")

E("verdict body",
  """      verdictKicker: tried ? 'The crew it needs' : 'Awaiting your attempt',
      verdictBig: tried ? crewN.toLocaleString() : '—',
      verdictBody: tried
        ? 'people, pulling exactly as hard as you just did, at the same instant. Your best was ' +
          Math.round(this.state.peak || max).toLocaleString() + ' lb. The stone needs ' + s.lb.toLocaleString() + ' lb.'
        : 'Hold the stone and pull. The meter is honest — for the heavy ones your whole body barely registers, which is the point.',
      peakLabel: tried ? (this.state.peak || max).toLocaleString() + ' lb' : '—',
      weightLabel: s.lb.toLocaleString() + ' lb',
      movedLabel: tried ? '0 in' : '—',""",
  """      verdictKicker: tried ? 'The crew it needs' : 'Awaiting your attempt',
      verdictBig: tried ? this.pushCrew(Math.round(this.state.peak || max)).toLocaleString() : '—',
      verdictBody: tried
        ? 'people, pushing exactly as hard as you just did, at the same instant, just to break it loose. Your best was ' +
          Math.round(this.state.peak || max).toLocaleString() + ' lb. Sliding this stone takes ' + this.breakaway().toLocaleString() +
          ' lb, and lifting it clear of the ground takes all ' + s.lb.toLocaleString() + '.'
        : 'Spin the stone, then hold PUSH. The striker is honest — for the heavy ones your whole body barely lifts the puck off the deck, which is the point.',
      peakLabel: tried ? (this.state.peak || max).toLocaleString() + ' lb' : '—',
      weightLabel: s.lb.toLocaleString() + ' lb',
      movedLabel: tried ? ((this._creep || 0) * 100 >= 0.5 ? (this._creep * 100).toFixed(1) + ' cm of creep' : '0 cm') : '—',""")

E("share prompt",
  "        : 'Try the lift first — your result goes on the card: your pull, what it needs, and the nothing you moved it.'),",
  "        : 'Try the striker first — your result goes on the card: your push, what it needs, and the nothing you moved it.'),")

E("section comment", "  /* ---------------- the lift ---------------- */", "  /* ---------------- the push ---------------- */")

E("share text",
  """    return 'I tried to lift ' + s.edition + '. My whole body pulls ' + peak.toLocaleString() +
      ' lb. It needs ' + s.lb.toLocaleString() + '. It did not move. — The Ancient Atlas';""",
  """    return 'I tried to push ' + s.edition + '. My whole body makes ' + peak.toLocaleString() +
      ' lb. Breaking it loose takes ' + this.breakaway().toLocaleString() + '. It did not move. — The Ancient Atlas';""")

E("share card rows",
  "    const rows = [['YOUR PULL', peak + ' LB'], ['IT NEEDS', s.lb.toLocaleString() + ' LB'], ['YOU MOVED IT', '0 IN']];",
  "    const rows = [['YOUR PUSH', peak + ' LB'], ['TO BUDGE IT', this.breakaway().toLocaleString() + ' LB'], ['YOU MOVED IT', '0 CM']];")

E("mobile meter label", "<span>Your pull</span>", "<span>Your push</span>")
E("verdict row label", "<span style=\"color:#8A8779\">Your peak pull</span>", "<span style=\"color:#8A8779\">Your peak push</span>")

E("aria", 'aria-label="Hold to lift"', 'aria-label="Hold to push"')
E("msg default", "Press and hold. Pull as hard as you can.", "Press and hold. Push as hard as you can.")


# ------------------------------------------------------------------ HUD
def hud(mobile):
    if mobile:
        pad, top, bot = "11px", "40px", "12px"
        bfont, bpad = "8.5px", "6px 8px"
        tube, srad, sbot = "20px", "10px", "62px"
        pfont, ppad = "11.5px", "13px 20px"
        chip = "8.5px"
        wrap = "normal"
    else:
        pad, top, bot = "16px", "48px", "16px"
        bfont, bpad = "9px", "8px 11px"
        tube, srad, sbot = "26px", "13px", "74px"
        pfont, ppad = "13px", "15px 32px"
        chip = "9.5px"
        wrap = "nowrap"

    btn = ("pointer-events:auto;font-family:'JetBrains Mono',monospace;font-size:" + bfont +
           ";letter-spacing:.14em;text-transform:uppercase;padding:" + bpad +
           ";border-radius:9px;cursor:pointer;user-select:none;-webkit-user-select:none;"
           "-webkit-tap-highlight-color:transparent;text-align:center;white-space:nowrap;"
           "backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);"
           "box-shadow:0 2px 0 rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.07);"
           "transition:background .18s,color .18s,border-color .18s,transform .08s;border:1px solid ")

    chipcss = ("font-family:'JetBrains Mono',monospace;font-size:" + chip +
               ";letter-spacing:.05em;line-height:1.5;color:#b9b3a3;background:rgba(9,9,13,.74);"
               "border:1px solid rgba(201,168,76,.2);border-radius:8px;padding:5px 9px;"
               "backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);white-space:" + wrap)

    tpl = """
      <!-- ============ in-frame controls ============================== -->
      <!-- Everything you can do to the stone now lives ON the stage. The
           cluster is a sibling of [data-stage] so drag-to-spin underneath
           is completely untouched: containers are pointer-events:none and
           only the buttons themselves take the pointer back. -->
      <div style="position:absolute;left:PAD;top:TOP;display:flex;flex-direction:column;gap:6px;z-index:7;pointer-events:none">
        <div sc-camel-on-click="{{ toggleSpin }}" role="button" tabindex="0" aria-label="Toggle rotation" style="BTN{{ spinBorder }};background:{{ spinBg }};color:{{ spinFg }}">{{ spinLabel }}</div>
        <div sc-camel-on-click="{{ resetView }}" role="button" tabindex="0" aria-label="Reset view" style="BTNrgba(201,168,76,.26);background:rgba(9,9,13,.72);color:#8A8779">Reset</div>
        <div sc-camel-on-click="{{ toggleCine }}" role="button" tabindex="0" aria-label="Cinematic view" style="BTN{{ cineBorder }};background:{{ cineBg }};color:{{ cineFg }}">{{ cineLabel }}</div>
      </div>

      <!-- ============ the high striker =============================== -->
      <!-- Bell at the top is breakaway force. The tube is LINEAR against
           it, which is the whole argument: a log scale would flatter the
           heavy stones into looking reachable. -->
      <div data-striker="" style="position:absolute;right:PAD;top:TOP;bottom:SBOT;display:flex;gap:7px;align-items:stretch;z-index:6;pointer-events:none">
        <div style="display:flex;flex-direction:column;justify-content:space-between;align-items:flex-end;text-align:right;padding:2px 0">
          <span style="font-family:'JetBrains Mono',monospace;font-size:CHIP;letter-spacing:.06em;color:#C9A84C;text-shadow:0 0 10px rgba(10,10,14,.95);white-space:nowrap">{{ strikerTop }}</span>
          <span data-striker-num="" style="font-family:'JetBrains Mono',monospace;font-size:CHIP;letter-spacing:.06em;color:#F3D998;text-shadow:0 0 10px rgba(10,10,14,.95);white-space:nowrap">0 %</span>
        </div>
        <div style="width:TUBE;display:flex;flex-direction:column;align-items:center;gap:5px">
          <i data-bell="" style="flex:none;width:TUBE;height:TUBE;border-radius:50%;border:1px solid rgba(232,185,96,.42);background:radial-gradient(circle at 38% 32%,rgba(58,50,29,.92),rgba(9,9,13,.94));box-shadow:inset 0 1px 0 rgba(255,255,255,.06);transition:background .2s,box-shadow .2s"></i>
          <div style="position:relative;flex:1;width:100%;border-radius:SRAD;background:linear-gradient(180deg,#050409,#0d0c14);border:1px solid rgba(201,168,76,.28);overflow:hidden;box-shadow:inset 0 2px 8px rgba(0,0,0,.95)">
            <i style="position:absolute;left:0;right:0;top:25%;height:1px;background:rgba(201,168,76,.16)"></i>
            <i style="position:absolute;left:0;right:0;top:50%;height:1px;background:rgba(201,168,76,.16)"></i>
            <i style="position:absolute;left:0;right:0;top:75%;height:1px;background:rgba(201,168,76,.16)"></i>
            <i data-striker-fill="" style="position:absolute;left:0;right:0;bottom:0;height:0%;background:linear-gradient(0deg,#8a6f28,#C9A84C 58%,#F3D998);box-shadow:0 0 16px rgba(232,185,96,.5)"></i>
            <i data-striker-best="" style="position:absolute;left:0;right:0;bottom:0;height:1px;background:#F3D998;opacity:0;box-shadow:0 0 8px rgba(243,217,152,.9)"></i>
          </div>
        </div>
      </div>

      <!-- ============ instructions + the push ======================== -->
      <div style="position:absolute;left:PAD;right:PAD;bottom:BOT;display:flex;align-items:flex-end;justify-content:space-between;gap:10px;z-index:7;pointer-events:none">
        <div style="display:flex;flex-direction:column;gap:5px;max-width:56%">
          <span style="CHIPCSS">{{ hintSpin }}</span>
          <span style="CHIPCSS">{{ hintPush }}</span>
        </div>
        <div sc-camel-on-pointer-down="{{ startHold }}" role="button" tabindex="0" aria-label="Hold to push" style="pointer-events:auto;flex:none;font-family:'JetBrains Mono',monospace;font-size:PFONT;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#241c07;padding:PPAD;border-radius:13px;cursor:pointer;user-select:none;-webkit-user-select:none;-webkit-tap-highlight-color:transparent;touch-action:none;background:linear-gradient(180deg,#F0CE74,#D8B152 46%,#C9A84C);border:1px solid #f0d78f;transform:{{ btnPress }};transition:transform .07s,box-shadow .07s;box-shadow:{{ btnShadow }}">{{ btnLabel }}</div>
      </div>
"""
    # ONE pass, longest token first. A chain of .replace() calls is wrong here
    # and fails silently: "BOT" is inside "SBOT" and "PAD" is inside "PPAD",
    # so an earlier replace mangles a later token into "S12px" / "P11px".
    # CSS drops invalid declarations without a word, so the striker simply
    # loses its bottom and the button loses its padding, and nothing anywhere
    # says why. Alternation is ordered by length, and re matches left to right.
    table = {"CHIPCSS": chipcss, "PFONT": pfont, "SBOT": sbot, "PPAD": ppad,
             "CHIP": chip, "TUBE": tube, "SRAD": srad, "BTN": btn,
             "PAD": pad, "TOP": top, "BOT": bot}
    return re.sub("CHIPCSS|PFONT|SBOT|PPAD|CHIP|TUBE|SRAD|BTN|PAD|TOP|BOT",
                  lambda m: table[m.group(0)], tpl)


def main():
    if not APP.exists():
        sys.exit("ABORT: app.html not found - run the extract step first")
    html = APP.read_text(encoding="utf-8")

    applied, already, missing = [], [], []
    # Test for the NEW text first. Several replacements keep the original line
    # and append to it, so `old` is still a substring after a successful pass -
    # checking `old` first would re-apply them on every run and duplicate a
    # const declaration, which is a hard SyntaxError rather than a cosmetic
    # bug. Order matters here; do not swap these branches.
    for label, old, new in edits:
        if new in html:
            already.append(label)
        elif old in html:
            html = html.replace(old, new)
            applied.append(label)
        else:
            missing.append(label)

    if missing:
        print("ABORT: these edits matched neither the old nor the new text:")
        for m in missing:
            print("    " + m)
        sys.exit(1)

    # ---- HUD insertion, by anchor line so long attribute strings never
    #      have to be reproduced byte-for-byte.
    lines = html.split("\n")

    def find(sub, hint=""):
        hits = [i for i, l in enumerate(lines) if sub in l]
        if len(hits) != 1:
            sys.exit("ABORT: anchor %r matched %d lines %s" % (sub, len(hits), hint))
        return hits[0]

    # Guard on a MARKUP-only attribute. Guarding on "data-striker-fill" would
    # self-trip, because the painter edit above introduces that same string as
    # a querySelector inside the script block.
    if 'data-bell=""' in html:
        print("  . HUD already inserted")
    else:
        # mobile: dust <i> is the last child of [data-quake]; the HUD goes in
        # after the </div> that closes it, as a child of [data-stagelayer].
        mi = find("left:50%;bottom:8%;width:44vw", "(mobile dust)")
        if "</div>" not in lines[mi + 1]:
            sys.exit("ABORT: unexpected mobile stage structure at line %d" % (mi + 2))
        di = find("left:50%;bottom:6%;width:34%", "(desktop dust)")
        # insert the later one first so the earlier index stays valid
        lines.insert(di + 1, hud(False))
        lines.insert(mi + 2, hud(True))
        print("  + HUD inserted into both stages")

    # desktop: the fading one-line hint is replaced by the persistent chips
    hi = [i for i, l in enumerate(lines) if "it turns as slowly as it weighs" in l]
    if hi:
        del lines[hi[0]]
        print("  - removed the fading desktop hint (superseded by the in-frame chips)")

    html = "\n".join(lines)
    APP.write_text(html, encoding="utf-8")

    print("\n  applied %d edits, %d already current" % (len(applied), len(already)))
    for a in applied:
        print("      + " + a)
    for a in already:
        print("      . " + a)

    strays = [i + 1 for i, l in enumerate(html.split("\n"))
              if re.search(r"\blift(ing|ed|s)?\b", l, re.I) and "liftCrew" not in l
              and "s.lift" not in l and "lift:" not in l]
    print("\n  remaining 'lift' mentions on lines: %s" % (strays or "none"))


if __name__ == "__main__":
    main()
