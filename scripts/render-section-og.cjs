const {chromium}=require('playwright');
const fs=require('fs'),path=require('path');
(async()=>{
const root=path.resolve(__dirname,'..'), items=JSON.parse(fs.readFileSync(path.join(root,'data/sharing-pages.json')));
const logo=fs.readFileSync(path.join(root,'public/index.html'),'utf8').match(/<div class="logo-box"[^>]*>\s*(<svg[\s\S]*?<\/svg>)/)[1];
const bg='data:image/webp;base64,'+fs.readFileSync(path.join(root,'public/assets/social/atlas-landscape.webp')).toString('base64');
const b=await chromium.launch({headless:true,channel:'chrome'}),p=await b.newPage({viewport:{width:1200,height:630}});
for(const item of items){
await p.setContent(`<style>*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#102023;color:#fff9ed;padding:56px 60px;font-family:Arial}.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}.shade{position:absolute;inset:0;background:linear-gradient(90deg,#06141588,transparent);z-index:-1}.brand{display:flex;gap:18px;align-items:center;font:54px Georgia}.mark{width:66px;height:66px}.mark svg{width:100%;height:100%}h1{font:100px/1.03 Georgia;letter-spacing:-3px;margin:65px 0 37px}p{font-size:34px;color:#f2dfb5;margin:0}</style><img class="bg" src="${bg}"><div class="shade"></div><div class="brand"><span class="mark">${logo}</span>Ancient Atlas</div><h1>${item.lines.join('<br>')}</h1><p>${item.subtitle}</p>`);
await p.locator('img').evaluate(i=>i.decode());await p.screenshot({path:path.join(root,`public/assets/social/${item.image}-og.png`)});
}await b.close();})();
