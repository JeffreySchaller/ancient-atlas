const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch();
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:900}});
  await page.addInitScript(()=>{localStorage.setItem('aa_welcomeSeen_v1','1');localStorage.setItem('atlas-analytics-v1','denied');});
  await page.route('https://theancientatlas.com/**',async route=>{
   const url=new URL(route.request().url());const p=path.join(process.cwd(),'public',url.pathname==='/'?'index.html':url.pathname);
   if(fs.existsSync(p)&&fs.statSync(p).isFile())await route.fulfill({path:p});
   else await route.abort();
  });
  await page.route('https://www.youtube.com/embed/**',route=>route.fulfill({contentType:'text/html',body:'<p>Player fixture</p>'}));
  await page.goto('https://theancientatlas.com/',{waitUntil:'domcontentloaded'});
  if(width<950) {
    await page.locator('#atlas-map-tools summary').click();
    await page.locator('#atlas-map-tools #atlas-analytics-settings').click();
    await page.locator('#atlas-analytics-panel [data-choice="denied"]').click();
    await page.evaluate(()=>window.atlasExploreMap());
  }
  await page.locator('.leaflet-control-attribution').waitFor();
  await page.waitForTimeout(1000);
  assert.equal(await page.locator('#mode-hint').count(),0);
  const summary=page.locator('#atlas-map-tools summary');
  await summary.click();
  await page.locator('#atlas-map-tools #atlas-analytics-settings').click();
  await page.locator('#atlas-analytics-panel').waitFor({state:'visible'});
  await page.locator('#atlas-analytics-panel [data-choice="denied"]').click();
  assert.equal(await summary.evaluate(e=>e===document.activeElement),true);
  await page.evaluate(()=>AtlasPlayer.open({id:'dFFlXj87EH4',title:'Yongning walkthrough',creator:'Ale',handle:'@AleTravel77'}));
  const check=async()=>{
   const player=await page.locator('#atlas-watch').boundingBox();
   const credits=await page.locator('.leaflet-control-attribution').boundingBox();
   assert.ok(player.y+player.height<=credits.y-7,'player must not cover map credits');
   assert.ok(player.x>=0&&player.x+player.width<=width,'player fits viewport');
  };
  await check();
  for(let i=0;i<4;i++){await page.locator('[data-position]').click();await check();}
  await page.locator('[data-min]').click();await check();
  await page.locator('[data-min]').click();await check();
  await page.locator('.aw-grip').focus();
  for(let i=0;i<30;i++)await page.keyboard.press('ArrowDown');
  await check();
  await page.screenshot({path:'map-corner-'+width+'.png',fullPage:true});
  await page.locator('[data-close]').click();
  assert.equal(await page.locator('#atlas-watch').count(),0);
  await page.close();
  console.log(width+'px map controls and player passed');
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
