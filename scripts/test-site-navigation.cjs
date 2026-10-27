const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({headless:true,channel:'chrome'});
for(const width of [390,1440]){
 const p=await b.newPage({viewport:{width,height:900}});
 for(const path of ['/library/true-monoliths.html','/library/','/creators/','/islands/corsica/','/sites/tipon.html','/patterns/','/photos/','/contact.html','/experiences/feel-the-weight/']){
  await p.goto('http://localhost:8765'+path,{waitUntil:'domcontentloaded'});
  await p.locator('.atlas-return').waitFor();
  const a=p.locator('.atlas-return');await a.scrollIntoViewIfNeeded();
  const visible=await a.evaluate(el=>{const r=el.getBoundingClientRect();const x=r.x+r.width/2,y=r.y+r.height/2;return el.contains(document.elementFromPoint(x,y));});
  console.log(width,path,visible?'reachable':'OBSCURED');
  if(!visible)throw Error('return obscured');
 }
 await p.goto('http://localhost:8765/');
 await p.waitForFunction(()=>typeof openLibraryDrawer==='function');
 await p.evaluate(()=>openLibraryDrawer('true-monoliths'));
 await p.waitForTimeout(500);
 const article=p.frameLocator('#library-drawer-iframe');
 await article.locator('.atlas-return').click();
 await p.waitForFunction(()=>!document.getElementById('library-drawer').classList.contains('open'));
 if(!p.url().endsWith('/'))throw Error('map navigated');
 console.log(width,'embedded article returns to existing map');
 await p.close();
}await b.close()})().catch(e=>{console.error(e);process.exit(1)});
