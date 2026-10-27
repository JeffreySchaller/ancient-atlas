// Render a fresh, reproducible sharing-card layout using the existing glyph assets.
const {chromium} = require('playwright');
const fs = require('fs');
const path = require('path');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const sites=JSON.parse(fs.readFileSync(path.join(root,'data/sites.json')));
 const creators=JSON.parse(fs.readFileSync(path.join(root,'data/creators.json')));
 const logo=fs.readFileSync(path.join(root,'public/index.html'),'utf8').match(/<div class="logo-box"[^>]*>\s*(<svg[\s\S]*?<\/svg>)/)[1];
 const glyph=id=>'data:image/webp;base64,'+fs.readFileSync(path.join(root,`public/assets/glyphs/${id}.webp`)).toString('base64');
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
 await page.setContent(`<html><style>*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:linear-gradient(115deg,#101416,#171e20);color:#f0eee9;font-family:Arial,sans-serif;padding:60px 66px}.brand{font-family:Georgia,serif;font-size:33px;display:flex;align-items:center;gap:15px}.star{display:block;width:46px;height:46px}.star svg{width:100%;height:100%}.main{display:flex;align-items:center;justify-content:space-between;margin-top:57px}h1{font:normal 66px/1.06 Georgia,serif;letter-spacing:-2px;margin:0 0 22px}.sub{font-size:22px;color:#b9c9c8;line-height:1.5;margin:0}.tiles{display:grid;grid-template-columns:122px 122px;gap:15px;transform:rotate(-5deg);margin-right:16px}.tiles img{width:122px;height:122px;border-radius:27px;box-shadow:0 10px 22px #0005}.tiles img:nth-child(even){transform:translateY(26px)}footer{position:absolute;bottom:48px;left:66px;right:66px;display:flex;justify-content:space-between;font-size:16px;color:#aab8b6}.url{color:#d9bd70}</style><body><div class="brand"><span class="star">${logo}</span>Ancient Atlas</div><div class="main"><div><h1>See the ancient world.<br>Look a little closer.</h1><p class="sub">Remarkable places. Independent creators.<br>Watch their films. Follow your curiosity.</p></div><div class="tiles">${['polygonal','flow','underground','rockcut'].map(id=>`<img src="${glyph(id)}">`).join('')}</div></div><footer><span>${sites.length} places · ${Object.keys(creators).length} creators</span><span class="url">theancientatlas.com</span></footer></body></html>`);
 await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
 await page.screenshot({path:path.join(root,'public/og-image.png')});
 await browser.close();
})();
