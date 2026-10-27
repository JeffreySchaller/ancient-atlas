/* A single player, independent of replaceable site panels. */
(() => {
  let panel, lastTrigger, drag;
  function place(x, y) {
    if (!panel) return;
    const box = panel.getBoundingClientRect();
    panel.style.left = Math.max(8, Math.min(x, innerWidth-box.width-8))+'px';
    panel.style.top = Math.max(8, Math.min(y, innerHeight-box.height-8))+'px';
    panel.style.right = panel.style.bottom = 'auto';
  }
  function fit() {
    if (panel) { const b=panel.getBoundingClientRect(); place(b.left,b.top); }
  }
  window.addEventListener('resize', fit);
  const esc = s => String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function close() {
    if (panel) panel.remove();
    panel = null; drag = null;
    if (lastTrigger?.isConnected) lastTrigger.focus();
  }
  window.AtlasPlayer = {close, open({id, title, creator, handle, start=0}) {
    if (!/^[\w-]{11}$/.test(id)) return;
    start = Math.max(0, Math.floor(Number(start) || 0));
    lastTrigger = document.activeElement;
    if (!panel) {
      panel = document.createElement('section');
      panel.id = 'atlas-watch';
      panel.setAttribute('aria-label', 'Film player');
      document.body.append(panel);
    }
    panel.classList.remove('compact');
    const url = `https://www.youtube.com/watch?v=${id}${start ? '&t='+start+'s' : ''}`;
    const channel = handle ? 'https://www.youtube.com/' + (handle.startsWith('@') ? handle : '@'+handle) : '';
    panel.innerHTML = `<div class="aw-bar"><button type="button" class="aw-grip" aria-label="Move player. Drag or use arrow keys." title="Drag to move · arrow keys">⠿</button><span class="aw-title" title="${esc(title)}">${esc(title)}</span><button type="button" data-position aria-label="Move player to another corner" title="Move to another corner">⌖</button><button type="button" data-min aria-label="Minimize player" aria-expanded="true" title="Minimize">−</button><button type="button" data-close aria-label="Close player" title="Close">×</button></div><div class="aw-screen"><iframe title="${esc(title)}" src="https://www.youtube.com/embed/${id}?autoplay=1&playsinline=1&rel=0&start=${start}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="aw-info">${channel ? `<a class="aw-credit" href="${esc(channel)}" target="_blank" rel="noopener" title="Visit ${esc(creator)} on YouTube">${esc(creator || 'Creator')} ↗</a>` : `<span class="aw-credit">${esc(creator || 'YouTube')}</span>`}<a href="${esc(url)}" target="_blank" rel="noopener" aria-label="Watch this film on YouTube">YouTube ↗</a>${window.atlasExploreMap ? '<button type="button" data-map>Map</button>' : '<a href="/">Map</a>'}</div>`;
    const grip = panel.querySelector('.aw-grip');
    grip.onpointerdown = e => {
      if(e.button !== 0) return;
      const b=panel.getBoundingClientRect();
      drag={x:e.clientX,y:e.clientY,left:b.left,top:b.top};
      grip.setPointerCapture(e.pointerId); panel.classList.add('aw-dragging');
    };
    grip.onpointermove = e => {
      if(drag) place(drag.left+e.clientX-drag.x,drag.top+e.clientY-drag.y);
    };
    const stop = () => {drag=null;panel?.classList.remove('aw-dragging');};
    grip.onpointerup = grip.onpointercancel = grip.onlostpointercapture = stop;
    grip.onkeydown = e => {
      const offsets={ArrowLeft:[-24,0],ArrowRight:[24,0],ArrowUp:[0,-24],ArrowDown:[0,24]};
      if(!offsets[e.key])return;
      e.preventDefault();const b=panel.getBoundingClientRect(), d=offsets[e.key];place(b.left+d[0],b.top+d[1]);
    };
    panel.querySelector('[data-position]').onclick = () => {
      const b=panel.getBoundingClientRect();
      const right=b.left+b.width/2>innerWidth/2, bottom=b.top+b.height/2>innerHeight/2;
      const corners=[[8,8],[innerWidth-b.width-8,8],[innerWidth-b.width-8,innerHeight-b.height-8],[8,innerHeight-b.height-8]];
      const current=bottom?(right?2:3):(right?1:0);
      place(...corners[(current+1)%4]);
    };
    panel.querySelector('[data-close]').onclick = close;
    panel.querySelector('[data-min]').onclick = e => {
      const compact = panel.classList.toggle('compact');
      e.currentTarget.textContent = compact ? '▢' : '−';
      e.currentTarget.setAttribute('aria-label', compact ? 'Expand player' : 'Minimize player');
      e.currentTarget.setAttribute('aria-expanded', String(!compact));
      e.currentTarget.title = compact ? 'Expand' : 'Minimize';
      fit();
    };
    panel.querySelector('[data-map]')?.addEventListener('click', () => window.atlasExploreMap());
    fit();
    window.atlasAnalytics?.('atlas_video_open', id);
  }};
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-atlas-video]');
    if (!a || !a.dataset.atlasVideo || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    window.AtlasPlayer.open({id:a.dataset.atlasVideo,title:a.dataset.title,creator:a.dataset.creator,handle:a.dataset.handle,start:a.dataset.start});
  });
  document.addEventListener('keydown', e => {if(e.key==='Escape' && panel) close();});
})();
