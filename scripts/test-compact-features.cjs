const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 for(const width of [390,1440]){
  const page=await browser.newPage({viewport:{width,height:900}});
  await page.goto('http://localhost:8765/');
  await page.waitForFunction(()=>typeof isProvisionalSite==='function');
  assert(await page.evaluate(()=>isProvisionalSite(SITES.find(s=>s.n==='Qiao Family Cave (Xichong, approximate)'))));
  assert(await page.evaluate(()=>markerCluster.getLayers().filter(m=>isProvisionalSite(m._site)).every(m=>m.options.icon.options.html.includes('atlas-provisional-symbol'))));
  await page.evaluate(()=>visitPanelSite('Qiao Family Cave (Xichong, approximate)'));
  const panel=page.locator(width===390?'#mss-body':'#detail');
  assert((await panel.textContent()).includes('Approximate area only.'));
  assert(await page.evaluate(()=>siteFeatureIds(SITES.find(s=>s.n==='Newgrange')).includes('sky')));
  for(const id of ['polygonal','joints','flow','underground','rockcut','sky']){
   const response=await page.request.get('http://localhost:8765/assets/glyphs/compact/'+id+'.svg');assert.equal(response.status(),200);
  }
  await page.evaluate(()=>visitPanelSite('Tipón'));
  await page.screenshot({path:'/tmp/atlas-compact-'+width+'.png'});
  console.log(width,'compact assets and provisional labels passed');
  await page.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
