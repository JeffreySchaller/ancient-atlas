#!/usr/bin/env python3
"""
Verifier for the Ancient Atlas conversations lane.  docs/CONVERSATIONS_SPEC.md

Its job is NOT to certify the good case. It is to reject the bad ones.
Each bad case asserts the RULE NUMBERS it must trigger, so a fixture cannot
pass for an unrelated incidental reason.

Run:  python3 scripts/verify-conversations.py
"""
import json, re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
def J(p): return json.loads((ROOT / p).read_text(encoding='utf-8'))

SC        = J('data/conversations.schema.json')
CREATORS  = J('data/creators.json')
_s        = J('data/sites.json'); _s = _s if isinstance(_s, list) else _s.get('sites', _s)
SITENAMES = {x.get('n') or x.get('name') for x in _s}
HOST      = SC['host_key']
IDPAT     = re.compile(SC['id_pattern'])
TODAY     = datetime.date.today()

# R1 is asserted over every copy of videos.json that exists, not just data/.
VIDEO_IDS, VIDEO_SRC = set(), []
for rel in SC['videos_copies']:
    f = ROOT / rel
    if f.exists():
        VIDEO_SRC.append(rel)
        VIDEO_IDS |= {v['id'] for vs in json.loads(f.read_text()).values() for v in vs}


def _iso(v):
    try:
        return datetime.date.fromisoformat(v)
    except Exception:
        return None


def check(entries, featured_id=None):
    """Return [(rule_no, message)]. Empty means pass."""
    f, seen = [], {}

    # R7 - the collection must exist at all. An empty file is not a pass.
    if len(entries) < SC['min_entries']:
        f.append((7, "conversations.json holds %d entries; the featured slot has "
                     "nothing to point at" % len(entries)))

    for i, c in enumerate(entries):
        who = c.get('episode') or (c.get('title') or '')[:38] or "entry %d" % i
        cid, status = c.get('id', ''), c.get('status')
        coming = status in SC['status_values']

        # ---- R6 id shape + uniqueness, for the episode AND its reply ----
        ids = [('id', cid)]
        rep = c.get('reply') or {}
        if rep:
            ids.append(('reply.id', rep.get('id', '')))
        for label, v in ids:
            if not v:
                continue
            if not IDPAT.match(v):
                f.append((6, "%s: %s %r is not %d URL-safe chars" % (who, label, v, SC['id_length'])))
            if v in seen:
                f.append((6, "%s: duplicate %s %s (also %s)" % (who, label, v, seen[v])))
            seen[v] = "%s/%s" % (who, label)
            # ---- R1 lane separation, replies included ----
            if v in VIDEO_IDS:
                f.append((1, "%s: %s %s is ALSO in videos.json (%s). A video is walked "
                             "or discussed, never both." % (who, label, v, ", ".join(VIDEO_SRC))))

        # ---- R2 guest resolves ----
        g = c.get('guest')
        if g not in CREATORS:
            f.append((2, "%s: guest %r is not a key in creators.json. Create the creator "
                         "record first." % (who, g)))
        # ---- R3 the swap test: the host is implicit ----
        if g == HOST:
            f.append((3, "%s: guest is %r. A conversation needs someone other than the host; "
                         "this looks like a walkthrough." % (who, HOST)))

        # ---- R4 sites resolve by exact match ----
        for s in c.get('sites') or []:
            n = s.get('n') if isinstance(s, dict) else s
            if n not in SITENAMES:
                f.append((4, "%s: site %r matches no name in sites.json. Exact match only; "
                             "sites.json is not ASCII-normalised (Kaymakli, Nemrut Dagi, "
                             "Agirnas all carry Turkish forms)." % (who, n)))

        # ---- R5 reachable, and the study must be a page that exists ----
        study = c.get('study')
        if not (c.get('sites') or study):
            f.append((5, "%s: unreachable. Needs at least one site or a study slug." % who))
        if study:
            page = ROOT / SC['study_page'].split()[0].format(slug=study)
            if not page.exists():
                f.append((5, "%s: study %r has no page at %s. A slug that resolves to "
                             "nothing is not reachability." % (who, study, page.relative_to(ROOT))))

        # ---- R8 release state ----
        pub = c.get('published')
        if cid and coming:
            f.append((8, "%s: has a real id AND status %r. Pick one." % (who, status)))
        if not cid and not coming:
            f.append((8, "%s: empty id requires status %s, got %r" % (who, SC['status_values'], status)))
        if cid and not pub:
            f.append((8, "%s: published id with no publish date" % who))
        for label, v in [('published', pub), ('recorded', c.get('recorded')),
                         ('reply.published', rep.get('published'))]:
            if v is None:
                continue
            d = _iso(v)
            if d is None:
                f.append((8, "%s: %s %r is not an ISO date" % (who, label, v)))
            elif label != 'recorded' and d > TODAY:
                f.append((8, "%s: %s %s is in the future" % (who, label, v)))

        # ---- R9 field hygiene ----
        for k in SC['required_fields']:
            if not c.get(k) and not (k == 'id' and coming):
                f.append((9, "%s: missing required field %r" % (who, k)))
        if cid:
            for k in SC['required_when_published']:
                if not c.get(k):
                    f.append((9, "%s: published entry missing %r" % (who, k)))
        for k in c:
            if k not in SC['allowed_fields'] and not k.startswith('_'):
                f.append((9, "%s: unknown field %r (schema allows %s)" % (who, k, SC['allowed_fields'])))
        for k in rep:
            if k not in SC['reply_fields']:
                f.append((9, "%s: unknown reply field %r" % (who, k)))

    # ---- R7 the featured slot is a pointer ----
    if featured_id:
        if featured_id not in {c.get('id') for c in entries}:
            f.append((7, "feature.json interview id %s is not in conversations.json. The "
                         "featured slot must point at a stored entry." % featured_id))
    return f


def report(label, fails, want_rules):
    """want_rules: set of rule numbers that MUST fire. empty set = must pass clean."""
    got = {r for r, _ in fails}
    ok = (not fails) if not want_rules else want_rules.issubset(got)
    print("  %-52s %s" % (label, "PASS" if ok else "*** WRONG ***"))
    if want_rules:
        print("        want R%s   fired R%s" % (sorted(want_rules), sorted(got) or "[]"))
    for r, m in fails:
        print("        R%d  %s" % (r, m))
    return ok


def main():
    live = J('data/conversations.json')['conversations']
    feat = J('data/feature.json').get('interview', {}).get('id') or None
    ok = True

    print("\nGOOD CASES (must pass clean)")
    ok &= report("live data/conversations.json + live feature pointer", check(live, feat), set())
    ok &= report("pre-release state: featured id cleared to ''", check(live, None), set())

    print("\nBAD CASES (must fire the named rules)")
    B = [
      ("a walkthrough smuggled in as a conversation", {1, 3},
       [{"id": "bnslsxXi3RY", "title": "Derinkuyu | Fieldwork Walkthrough", "guest": HOST,
         "episode": "EP01", "published": "2026-06-10", "sites": [{"n": "Derinkuyu Underground City"}]}], None),
      ("a reply carrying a walkthrough id, dated forward", {1, 8},
       [{"id": "AAAAAAAAAAA", "title": "x", "guest": "agelessrock", "episode": "CCA",
         "published": "2026-01-01", "study": "ageless-rock",
         "reply": {"id": "bnslsxXi3RY", "published": "2099-12-31"}}], None),
      ("site that does not exist (near-miss spelling)", {4},
       [{"id": "BBBBBBBBBBB", "title": "x", "guest": "agelessrock", "episode": "CCB",
         "published": "2026-01-01", "sites": [{"n": "Kaymakli Underground Citty"}]}], None),
      ("guest with no creator record (the real Brent case)", {2},
       [{"id": "CCCCCCCCCCC", "title": "x", "guest": "brentslava", "episode": "CCC",
         "published": "2026-01-01", "sites": [{"n": "Machu Picchu"}]}], None),
      ("study slug pointing at a page that does not exist", {5},
       [{"id": "DDDDDDDDDDD", "title": "x", "guest": "stoneriddles", "episode": "CCD",
         "published": "2026-01-01", "study": "this-study-does-not-exist"}], None),
      ("no sites and no study -- unreachable", {5},
       [{"id": "EEEEEEEEEEE", "title": "x", "guest": "stoneriddles", "episode": "CCE",
         "published": "2026-01-01"}], None),
      ("truncated id", {6},
       [{"id": "SHORT", "title": "x", "guest": "stoneriddles", "episode": "CCF",
         "published": "2026-01-01", "sites": [{"n": "Machu Picchu"}]}], None),
      ("future-dated release instead of status coming", {8},
       [{"id": "FFFFFFFFFFF", "title": "x", "guest": "sorcerersofstone", "episode": "CCG",
         "published": "2099-01-01", "sites": [{"n": "Machu Picchu"}]}], None),
      ("empty id with no status", {8},
       [{"id": "", "title": "x", "guest": "sorcerersofstone", "episode": "CCH",
         "sites": [{"n": "Machu Picchu"}]}], None),
      ("real id AND status coming -- contradictory", {8},
       [{"id": "GGGGGGGGGGG", "status": "coming", "title": "x", "guest": "sorcerersofstone",
         "episode": "CCI", "published": "2026-01-01", "sites": [{"n": "Machu Picchu"}]}], None),
      ("published entry with no publish date", {8, 9},
       [{"id": "HHHHHHHHHHH", "title": "x", "guest": "stoneriddles", "episode": "CCJ",
         "sites": [{"n": "Machu Picchu"}]}], None),
      ("invented field the schema does not allow", {9},
       [{"id": "IIIIIIIIIII", "title": "x", "guest": "stoneriddles", "episode": "CCK",
         "published": "2026-01-01", "sites": [{"n": "Machu Picchu"}], "totally_made_up": 1}], None),
      ("the same episode entered twice", {6}, [dict(live[0]), dict(live[0])], feat),
      ("featured pointer aiming at nothing", {7}, live, "ZZZZZZZZZZZ"),
      ("an EMPTY collection -- the case that used to pass", {7}, [], None),
    ]
    for label, want, entries, fid in B:
        ok &= report(label, check(entries, fid), want)

    print("\nNOT MECHANIZED -- needs a person:")
    for l in ["was the camera actually AT the site (R1 is the judgement call)",
              "whether a site is genuinely discussed or merely name-dropped",
              "whether the guest warrants tier 1/2/3 in creators.json",
              "whether the study page actually covers this episode"]:
        print("    - " + l)

    print("\n%s\n" % ("ALL CASES BEHAVED AS ASSERTED" if ok else
                      "*** THE VERIFIER IS WRONG - a case did not behave as asserted ***"))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
