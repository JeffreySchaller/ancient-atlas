// Run with a local server serving public/ on port 8765 and Playwright installed.
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const width of [390,1440]){
 await page.setViewportSize({width,height:900});
 await page.goto('http://localhost:8765/sites/longroiva-castle.html');
 console.log('static',width,await page.locator('.film-credit').innerText(),await page.locator('.vid').getAttribute('href'),await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(await page.locator('.vid').getAttribute('target')!=='_blank')throw Error('video replaces Atlas');
 if(!(await page.locator('a[href="/creators/ancient-atlas.html"]').count()))throw Error('missing own films');

 }
 await page.goto('http://localhost:8765/?site=Longroiva%20Castle');
 await page.waitForFunction(()=>typeof showDetail==='function');
 await page.evaluate(()=>showDetail(SITES.find(s=>s.n==='Longroiva Castle')));
 console.log('desktop credit',await page.locator('#detail .journey-link').allTextContents());
 console.log('mobile render',await page.evaluate(()=>{
 const site=SITES.find(s=>s.n==='Longroiva Castle');showMobileSiteSheet(site);
 return {sheet:document.querySelector('#mss-body').innerText,feed:renderMobileSiteSection(site.n,site,VIDEOS[site.n]).includes('More from Ageless Rock')};
 }));
 let opened=0;await page.route('https://www.youtube.com/**',r=>r.fulfill({body:'Video destination'}));page.context().on('page',()=>opened++);
 await page.evaluate(()=>openYouTubeVideo('sJ7fhhe9F6I',235));await page.waitForTimeout(1000);
 if(opened!==1)throw Error('Expected one new tab; got '+opened);
 console.log('single video tab',opened,'errors',errors);
 if(errors.length)throw Error(errors.join('\n'));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
