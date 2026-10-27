// Render the sharing card with large, legible type over its Higgsfield background.
const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const logo=fs.readFileSync(path.join(root,'public/index.html'),'utf8').match(/<div class="logo-box"[^>]*>\s*(<svg[\s\S]*?<\/svg>)/)[1];
 const bg='data:image/webp;base64,'+fs.readFileSync(path.join(root,'public/assets/social/atlas-landscape.webp')).toString('base64');
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
 await page.setContent(`<html><style>*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#102023;color:#fff9ed;font-family:Arial,sans-serif;padding:56px 60px}.backdrop{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}.shade{position:absolute;inset:0;background:linear-gradient(90deg,#06141555,transparent 75%);z-index:-1}.brand{display:flex;align-items:center;gap:18px;font:54px Georgia,serif}.mark{width:66px;height:66px;display:block}.mark svg{width:100%;height:100%}h1{font:normal 108px/1.03 Georgia,serif;letter-spacing:-3px;margin:65px 0 37px;text-shadow:0 2px 12px #06141555}.invitation{margin:0;font-size:38px;line-height:1.3;color:#f2dfb5;letter-spacing:-.5px}</style><body><img class="backdrop" src="${bg}" alt=""><div class="shade"></div><div class="brand"><span class="mark">${logo}</span>Ancient Atlas</div><h1>See the<br>ancient world.</h1><p class="invitation">Watch films. Find your next journey.</p></body></html>`);
 await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
 await page.screenshot({path:path.join(root,'public/og-image.png')});
 // Preview the actual card at common messaging-card width, without changing the asset.
 const card=await page.screenshot();
 await page.setViewportSize({width:400,height:210});
 await page.setContent(`<body style="margin:0"><img width="400" height="210" src="data:image/png;base64,${card.toString('base64')}"></body>`);
 await page.locator('img').evaluate(i=>i.decode());
 await page.screenshot({path:'/tmp/atlas-og-message-preview.png'});
 await browser.close();
})();
