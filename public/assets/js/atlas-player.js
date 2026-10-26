/* A single player, independent of replaceable site panels. */
(() => {
  let panel, lastTrigger;
  const esc = s => String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function close() {
    if (panel) panel.remove();
    panel = null;
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
    panel.innerHTML = `<div class="aw-bar"><span>Watch while you explore</span><button type="button" data-min aria-label="Minimize player" aria-expanded="true">Minimize</button><button type="button" data-close aria-label="Close player">×</button></div><div class="aw-screen"><iframe title="${esc(title)}" src="https://www.youtube.com/embed/${id}?autoplay=1&playsinline=1&rel=0&start=${start}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="aw-info"><strong>${esc(title)}</strong><span>Film by ${esc(creator || 'YouTube')}</span><div><a href="${esc(url)}" target="_blank" rel="noopener">Watch on YouTube ↗</a>${channel ? `<a href="${esc(channel)}" target="_blank" rel="noopener">${esc(creator)}’s channel ↗</a>` : ''}${window.atlasExploreMap ? '<button type="button" data-map>Explore map</button>' : '<a href="/">Explore the Atlas map →</a>'}</div></div>`;
    panel.querySelector('[data-close]').onclick = close;
    panel.querySelector('[data-min]').onclick = e => {
      const compact = panel.classList.toggle('compact');
      e.currentTarget.textContent = compact ? 'Expand' : 'Minimize';
      e.currentTarget.setAttribute('aria-label', compact ? 'Expand player' : 'Minimize player');
      e.currentTarget.setAttribute('aria-expanded', String(!compact));
    };
    panel.querySelector('[data-map]')?.addEventListener('click', () => window.atlasExploreMap());
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
