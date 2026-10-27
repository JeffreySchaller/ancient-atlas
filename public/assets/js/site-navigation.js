/* Shared return route; embedded articles return to their existing map. */
(() => {
  let wired=false;
  function init() {
    if(document.querySelector('.atlas-return') || !document.body)return;
    if(!document.querySelector('link[href="/assets/site-navigation.css"]')){
      const css=document.createElement('link');css.rel='stylesheet';css.href='/assets/site-navigation.css';document.head.append(css);
    }
    const rootLinks=[...document.querySelectorAll('header a, nav a')].filter(a=>{
      const u=new URL(a.href,location.href);
      return u.origin===location.origin && (u.pathname==='/'||u.pathname==='/index.html')&&!u.search;
    });
    let back=rootLinks.find(a=>/^(atlas|map|back to map)$/i.test(a.textContent.trim()));
    if(!back){
      back=document.createElement('a');back.href='/';
      const host=document.querySelector('header nav, nav') || document.querySelector('header');
      if(host)host.append(back);
      else {const rail=document.createElement('div');rail.className='atlas-return-rail';rail.append(back);document.body.prepend(rail);}
    }
    back.classList.add('atlas-return');back.textContent='← Back to map';
    back.setAttribute('aria-label','Back to the Ancient Atlas map');
    if(wired)return;wired=true;
    document.addEventListener('click',e=>{
      const a=e.target.closest('a');if(!a||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
      const u=new URL(a.href,location.href);
      if(window.parent!==window && u.origin===location.origin && (u.pathname==='/'||u.pathname==='/index.html')&&!u.search){
        e.preventDefault();window.parent.postMessage({type:'atlas:return-to-map'},location.origin);
      }
    });
    document.addEventListener('keydown',e=>{
      if(e.key==='Escape'&&window.parent!==window)window.parent.postMessage({type:'atlas:return-to-map'},location.origin);
    });
  }
  // Packaged experiences replace their document and render asynchronously.
  if(location.pathname.startsWith('/experiences/')){
    let pending=false;
    new MutationObserver(()=>{
      if(pending||document.querySelector('.atlas-return'))return;
      pending=true;setTimeout(()=>{pending=false;init();},150);
    }).observe(document,{childList:true,subtree:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
