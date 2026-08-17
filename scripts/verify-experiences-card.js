/*
 * verify.js - load the built bundle in headless Chrome and assert on the
 * LIVE dom, after the unpacker has swapped the document.
 *
 * --dump-dom is useless here: it snapshots at load, long before the async
 * unpack finishes, so it always reports the placeholder. This drives Chrome
 * over CDP instead and waits for the real page. Node 21+ ships a global
 * WebSocket, so there is no dependency to install.
 *
 *   node scripts/ftw/verify.js [width height]
 */
const { spawn } = require('child_process');
const http = require('http');
const path = require('path');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const W = +(process.argv[2] || 1440), H = +(process.argv[3] || 950);
const FILE = 'file://' + encodeURI(path.resolve(__dirname, '../public/index.html'));

const sleep = ms => new Promise(r => setTimeout(r, ms));

function getJSON(url) {
  return new Promise((res, rej) => {
    http.get(url, r => { let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d))); }).on('error', rej);
  });
}

(async () => {
  try { require('child_process').execSync("pkill -f 'remote-debugging-port=" + PORT + "'"); } catch (e) {}
  await sleep(1200);
  const chrome = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--no-sandbox',
    '--use-gl=swiftshader', '--enable-unsafe-swiftshader',
    '--allow-file-access-from-files',
    // A FIXED profile dir lets Chromium serve a cached copy of the bundle, so a
    // verification run can happily report on the previous build. That is worse
    // than no verification at all. Fresh profile every run.
    '--user-data-dir=/tmp/ftwverify-' + process.pid + '-' + Math.floor(Math.random() * 1e6),
    '--disk-cache-size=1',
    '--remote-debugging-port=' + PORT,
    '--window-size=' + W + ',' + H,
    FILE,
  ], { stdio: 'ignore' });

  let targets = null;
  for (let i = 0; i < 40 && !targets; i++) {
    await sleep(500);
    try { targets = (await getJSON('http://127.0.0.1:' + PORT + '/json')).filter(t => t.type === 'page'); } catch (e) {}
  }
  if (!targets || !targets.length) { console.log('ABORT: no CDP page target'); chrome.kill(); process.exit(1); }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 0; const waiting = new Map();
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
  };
  const send = (method, params) => new Promise(r => {
    const n = ++id; waiting.set(n, r); ws.send(JSON.stringify({ id: n, method, params }));
  });
  const evalJS = async expr => {
    const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.result && r.result.exceptionDetails) return { __throw: r.result.exceptionDetails.text };
    return r.result && r.result.result ? r.result.result.value : null;
  };

  await send('Runtime.enable');
  await sleep(6000);   // unpack + THREE boot + first frames

  const geo = await evalJS(`(function(){
    const t = document.querySelector('.fw-wrap .nav-tile');
    if (!t) return null;
    const r = t.getBoundingClientRect();
    return { x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2) };
  })()`);
  if (!geo) { console.log('ABORT: no Experiences tile'); process.exit(1); }

  // a real mouse move, because :hover does not respond to synthetic clicks
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: geo.x, y: geo.y, buttons: 0 });
  await sleep(1600);

  console.log(JSON.stringify(await evalJS(`(function(){
    const b = document.querySelector('.fw-bloom');
    if (!b) return { err: 'no bloom' };
    const cs = getComputedStyle(b);
    const r = b.getBoundingClientRect();
    const fv = [...document.querySelectorAll('.fw-fv')];
    const shown = fv.filter(e => +getComputedStyle(e).opacity > 0.5).length;
    const txt = (b.innerText || '').trim();
    return {
      visible: cs.opacity, box: Math.round(r.width) + 'x' + Math.round(r.height),
      offscreenRight: Math.round(r.right) > innerWidth,
      trucks: fv.length, trucksVisible: shown,
      truckBox: fv.length ? Math.round(fv[0].getBoundingClientRect().width) + 'x'
        + Math.round(fv[0].getBoundingClientRect().height) : null,
      text: txt,
      digits: txt.replace(/F-150/g, '').match(/[0-9]+/g) || []
    };
  })()`), null, 1));

  const fs = require('fs');
  const shot = await send('Page.captureScreenshot', { format: 'png',
    clip: { x: geo.x - 210, y: geo.y - 20, width: 420, height: 460, scale: 2 } });
  fs.writeFileSync('/tmp/fw-card.png', Buffer.from(shot.result.data, 'base64'));
  console.log('shot /tmp/fw-card.png');
  ws.close(); chrome.kill(); process.exit(0);
})();
