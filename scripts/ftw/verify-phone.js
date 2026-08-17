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
const FILE = 'file://' + encodeURI(path.resolve(__dirname, '../../public/experiences/feel-the-weight/index.html'));

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
  await send('Emulation.setDeviceMetricsOverride', {
    width: W, height: H, deviceScaleFactor: 3, mobile: true,
    screenWidth: W, screenHeight: H });
  await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await sleep(10000);   // unpack + THREE boot + first frames

  const probe = `(function(){
  const txt = el => el ? (el.innerText || el.textContent || '').trim() : null;
  const secs = [...document.querySelectorAll('[data-screen-label]')]
    .filter(s => s.getBoundingClientRect().height > 0)
    .map(s => s.dataset.screenLabel);

  // anything wider than the phone is a bug you only find by measuring
  const vw = document.documentElement.clientWidth;
  const wide = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > vw + 1 && r.height > 0) {
      wide.push((el.tagName.toLowerCase()) + (el.dataset.screenLabel ? '[' + el.dataset.screenLabel + ']' : '')
        + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : '')
        + ' ' + Math.round(r.width) + 'px');
    }
  });

  const h1 = document.querySelector('h1');
  const swatch = document.querySelector('[data-swatch]');
  const field = document.querySelector('[data-trucks]');
  const dock = document.querySelector('[data-dock]');
  const photo = document.querySelector('[data-photo]');
  const cards = [...document.querySelectorAll('[data-screen-label="06 If you keep looking"] h3')];
  const flags = [...document.querySelectorAll('[aria-label^="Weigh it in"]')];
  const box = el => { if (!el) return null; const r = el.getBoundingClientRect();
    return Math.round(r.left) + ',' + Math.round(r.top + scrollY) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height); };

  return {
    viewport: vw + 'x' + innerHeight,
    isPhoneLayout: secs.some(s => s.indexOf('M01') === 0),
    sections: secs,
    scrollWidth: document.documentElement.scrollWidth,
    overflowing: wide.slice(0, 10),
    h1: txt(h1), h1em: txt(h1 && h1.querySelector('em')), h1box: box(h1),
    said: txt(document.querySelector('h1 + p')),
    stage: box(document.querySelector('[data-stage]')),
    flagsBox: flags.map(box),
    swatch: txt(swatch), swatchBox: box(swatch),
    trucks: field ? field.querySelectorAll('svg').length : null, fieldBox: box(field),
    cards: cards.length, cardW: cards.length ? Math.round(cards[0].getBoundingClientRect().width) : null,
    dock: box(dock),
    photoLoaded: photo ? photo.naturalWidth > 0 : null, photoBox: box(photo),
    docHeight: document.documentElement.scrollHeight,
    unresolved: (document.body.innerHTML.match(/\{\{[^}]+\}\}/g) || []).slice(0, 6)
  };
})()`;

  console.log('-- phone render --');
  console.log(JSON.stringify(await evalJS(probe), null, 1));

  const fs = require('fs');
  for (const [name, y] of [['p1', 0], ['p2', 700], ['p3', 1500], ['p4', 2400]]) {
    await evalJS('scrollTo(0,' + y + ')');
    await sleep(800);
    const r = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('/tmp/ftw-' + name + '.png', Buffer.from(r.result.data, 'base64'));
  }
  await evalJS('document.getElementById("fw-real") && document.getElementById("fw-real").scrollIntoView()');
  await sleep(2500);
  console.log('photo after scroll: ' + JSON.stringify(await evalJS(
    '(function(){const p=document.querySelector("[data-photo]");if(!p)return null;const r=p.getBoundingClientRect();return {loaded:p.naturalWidth>0,w:Math.round(r.width),h:Math.round(r.height)};})()')));
  console.log('shots written');
  ws.close(); chrome.kill(); process.exit(0);
})();
