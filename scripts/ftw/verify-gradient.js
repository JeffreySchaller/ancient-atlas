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
  await sleep(9000);   // unpack + THREE boot + first frames

  const probe = `(function(){
  const txt = el => el ? (el.innerText || el.textContent || '').trim() : null;
  const secs = [...document.querySelectorAll('[data-screen-label]')]
    .filter(s => s.offsetParent !== null || s.getBoundingClientRect().height > 0)
    .map(s => ({ label: s.dataset.screenLabel, top: Math.round(s.getBoundingClientRect().top + scrollY) }));

  const pills = [...document.querySelectorAll('button')]
    .filter(b => b.querySelector('svg path') && b.textContent.trim().length && b.closest('[data-screen-label="D01 Specimen"]'))
    .map(b => ({ t: b.textContent.trim(), glyph: !!(b.querySelector('svg path') || {}).getAttribute }));

  const flags = [...document.querySelectorAll('[aria-label^="Weigh it in"]')].map(b => b.getAttribute('aria-label'));
  const swatch = document.querySelector('[data-swatch]');
  const field = document.querySelector('[data-trucks]');
  const cards = [...document.querySelectorAll('[data-screen-label="06 If you keep looking"] h3')].map(txt);
  const photo = document.querySelector('[data-photo]');

  const vis = document.body.innerText || '';
  const bad = ['hold to push','press and hold','hold push','striker','push as hard'];
  const badHits = bad.filter(w => vis.toLowerCase().includes(w));
  const digitLines = vis.split(String.fromCharCode(10)).map(l => l.trim())
    .filter(l => l && /[0-9]/.test(l));

  const weightSec = secs.find(s => s.label === '05 What it weighs');
  return {
    sections: secs.map(s => s.label),
    tops: secs.map(s => s.label + '@' + s.top),
    h1: txt(document.querySelector('h1')),
    said: txt(document.querySelector('[data-screen-label="D01 Specimen"] h1 + p')),
    matterAndDoor: txt(document.querySelector('a[href="#fw-weight"]')),
    pills: pills.map(p => p.t), pillGlyphs: pills.length,
    flags,
    swatch: txt(swatch),
    trucks: field ? field.querySelectorAll('svg').length : null,
    truckHead: txt(document.querySelector('#fw-weight p')),
    cards,
    photoLoaded: photo ? (photo.naturalWidth > 0) : null,
    photoTop: photo ? Math.round(photo.getBoundingClientRect().top + scrollY) : null,
    weightTop: weightSec ? weightSec.top : null,
    viewport: innerHeight,
    badHits,
    digitLines,
    unresolved: (document.body.innerHTML.match(/\{\{[^}]+\}\}/g) || []).slice(0, 8)
  };
})()`;

  console.log('-- render --');
  console.log(JSON.stringify(await evalJS(probe), null, 1));

  const clickFlag = i => `(function(){const b=document.querySelectorAll('[aria-label^="Weigh it in"]')[${i}];if(!b)return 'missing';b.click();return 'clicked';})()`;
  const readSwap = `(function(){
    const s = document.querySelector('[data-swatch]');
    const f = document.querySelector('[data-trucks]');
    return { swatch: s ? (s.innerText||'').trim() : null,
             anim: s ? (s.style.animation || getComputedStyle(s).animationName) : null,
             trucks: f ? f.querySelectorAll('svg').length : null };
  })()`;

  for (const [i, name] of [[1,'UK'],[2,'AU'],[0,'US']]) {
    console.log('-- switch to ' + name + ' --');
    console.log(JSON.stringify(await evalJS(clickFlag(i))));
    await sleep(700);
    console.log(JSON.stringify(await evalJS(readSwap)));
  }

  const fs = require('fs');
  await evalJS('scrollTo(0,0)'); await sleep(400);
  for (const [name, y] of [['band12', 0], ['band34', 1180]]) {
    await evalJS('scrollTo(0,' + y + ')');
    await sleep(900);
    const r = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('/tmp/ftw-' + name + '.png', Buffer.from(r.result.data, 'base64'));
    console.log('shot /tmp/ftw-' + name + '.png');
  }

  ws.close(); chrome.kill(); process.exit(0);
})();
