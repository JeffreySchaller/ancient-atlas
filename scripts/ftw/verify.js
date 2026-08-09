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
  const chrome = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--no-sandbox',
    '--use-gl=swiftshader', '--enable-unsafe-swiftshader',
    '--allow-file-access-from-files',
    '--user-data-dir=/tmp/ftwverify',
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
    var q=function(s){return document.querySelectorAll(s).length};
    var txt=function(s){var e=document.querySelector(s);return e?e.textContent.trim():null};
    return {
      title: document.title,
      err: (document.getElementById('__bundler_err')||{}).textContent || null,
      unpackFailed: /Error unpacking/.test(document.body.innerText||''),
      canvas: q('canvas'),
      stage: q('[data-stage]'),
      bell: q('[data-bell]'), fill: q('[data-striker-fill]'), best: q('[data-striker-best]'),
      buttons: [].slice.call(document.querySelectorAll('div[role=button]')).map(function(e){return e.getAttribute('aria-label')}),
      strikerCrew: txt('[data-striker] > div > span'),
      strikerNum: txt('[data-striker-num]'),
      need: txt('[data-need]'),
      pushBtn: txt('div[aria-label="Hold to push"]'),
      hints: [].slice.call(document.querySelectorAll('span')).map(function(e){return e.textContent.trim()}).filter(function(t){return /spin it|Hold PUSH/.test(t)}).slice(0,4),
      msg: txt('[data-msg]'),
      unresolved: (document.body.innerHTML.match(/\\{\\{\\s*\\w+/g)||[]).slice(0,6),
      consoleErr: window.__ftwErrs || null
    };
  })()`;
  console.log(JSON.stringify(await evalJS(probe), null, 1));

  // exercise the controls
  console.log('-- click SPIN, RESET, CINEMA, then hold PUSH --');
  console.log(JSON.stringify(await evalJS(`(function(){
    var byLabel=function(l){return document.querySelector('div[aria-label="'+l+'"]')};
    var out={};
    try{ byLabel('Toggle rotation').click(); out.spin='clicked'; }catch(e){ out.spin='ERR '+e.message }
    try{ byLabel('Reset view').click(); out.reset='clicked'; }catch(e){ out.reset='ERR '+e.message }
    try{ byLabel('Cinematic view').click(); out.cine='clicked'; }catch(e){ out.cine='ERR '+e.message }
    return out;
  })()`)));
  await sleep(1200);
  console.log(JSON.stringify(await evalJS(`(function(){
    var t=function(s){var e=document.querySelector(s);return e?e.textContent.trim():null};
    return {spinLabel:t('div[aria-label="Toggle rotation"]'), cineLabel:t('div[aria-label="Cinematic view"]'),
            err:(document.getElementById('__bundler_err')||{}).textContent||null};
  })()`)));


  // --- exercise the striker itself -------------------------------------
  console.log('-- hold PUSH on the Giza block --');
  await evalJS(`(function(){
    var b=document.querySelector('div[aria-label="Hold to push"]');
    b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,pointerType:'mouse'}));
    return 1;})()`);
  await sleep(1400);
  console.log(JSON.stringify(await evalJS(`(function(){
    var t=function(s){var e=document.querySelector(s);return e?e.textContent.trim():null};
    var f=document.querySelector('[data-striker-fill]');
    return {midFill:f?f.style.height:null, midNum:t('[data-striker-num]'), midMsg:t('[data-msg]')};
  })()`)));
  await sleep(1600);   // past GIVE_AT
  console.log(JSON.stringify(await evalJS(`(function(){
    var t=function(s){var e=document.querySelector(s);return e?e.textContent.trim():null};
    return {tomb:[t('[data-tomb1]'),t('[data-tomb2]'),t('[data-tomb3]'),t('[data-tomb4]')],
            crew:t('[data-crew]'), best:document.querySelector('[data-striker-best]').style.bottom,
            err:(document.getElementById('__bundler_err')||{}).textContent||null};
  })()`), null, 1));

  console.log('-- switch to the Forgotten Stone and push again --');
  await evalJS(`(function(){
    var b=[].slice.call(document.querySelectorAll('button')).filter(function(e){return /Forgotten/.test(e.textContent)})[0];
    b.click(); return 1;})()`);
  await sleep(1500);
  await evalJS(`(function(){
    var b=document.querySelector('div[aria-label="Hold to push"]');
    b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,pointerType:'mouse'}));
    return 1;})()`);
  await sleep(3000);
  console.log(JSON.stringify(await evalJS(`(function(){
    var t=function(s){var e=document.querySelector(s);return e?e.textContent.trim():null};
    return {crewLabel:t('[data-striker] > div > span'), num:t('[data-striker-num]'),
            need:t('[data-need]'), tomb:[t('[data-tomb2]'),t('[data-tomb3]'),t('[data-tomb4]')],
            crew:t('[data-crew]'), err:(document.getElementById('__bundler_err')||{}).textContent||null};
  })()`), null, 1));

  chrome.kill();
  process.exit(0);
})();
