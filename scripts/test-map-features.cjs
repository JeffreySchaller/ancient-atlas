const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 for(const width of [390,1440]){
  const page=await browser.newPage({viewport:{width,height:900}}), errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.route('https://www.youtube.com/embed/**',r=>r.fulfill({body:'Mock film'}));
  await page.goto('http://localhost:8765/?site=Tip%C3%B3n');
  await page.waitForFunction(()=>window.AtlasPlayer && document.querySelector('.atlas-feature-options'));
  const browserPanel=page.locator('.atlas-feature-browser:visible').first();
  await browserPanel.getByRole('button',{name:'Water channels'}).click();
  assert.deepEqual(await page.evaluate(()=>getFiltered().map(s=>s.n).sort()),['Petra','Tipón']);
  await browserPanel.getByRole('button',{name:'Clear feature'}).click();
  assert((await page.evaluate(()=>getFiltered().length))>600);
  await browserPanel.getByRole('button',{name:'Polygonal walls'}).click();
  assert(await page.evaluate(()=>getFiltered().every(s=>s.criteria.includes('polygonal'))));
  await browserPanel.getByRole('button',{name:'Clear feature'}).click();
  await page.evaluate(()=>visitPanelSite('Tipón'));
  const panel=page.locator(width===390?'#mss-body .oga-panel':'#detail .oga-panel');
  await panel.getByRole('button',{name:'Water channels',exact:true}).click();
  assert(await panel.locator('.oga-watch').first().evaluate(e=>e===document.activeElement));
  assert((await panel.textContent()).includes('Earth Explorer'));
  assert((await panel.textContent()).includes('Brien Foerster'));
  await panel.locator('[data-film-creator="earthexplorer"] .oga-watch').count().then(async n=>{
    if(n) await panel.locator('[data-film-creator="earthexplorer"] .oga-watch').click();
    else await panel.locator('.oga-watch').last().click();
  });
  await page.locator('#atlas-watch iframe').waitFor();
  assert((await page.locator('#atlas-watch').textContent()).includes('Earth Explorer'));
  const frame=await page.locator('#atlas-watch iframe').elementHandle();
  await page.evaluate(()=>chooseAtlasFeature('flow'));
  assert(await frame.evaluate(e=>e.isConnected));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  assert.deepEqual(errors,[]);
  console.log(width,'feature filters, clear, badges, creator credits and persistent playback passed');
  await page.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
