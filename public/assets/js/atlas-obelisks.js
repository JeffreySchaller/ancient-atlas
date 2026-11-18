(() => {
  'use strict';

  const glyph = '<svg viewBox="0 0 24 32" aria-hidden="true"><path d="M8 27 9 8 12 3 15 8 16 27Z M9 8h6 M6 28h12"/></svg>';
  const labels = {
    pharaonic: 'Pharaonic Egyptian', ptolemaic: 'Ptolemaic Egyptian',
    roman: 'Roman commission', egyptian_undated: 'Ancient; date uncertain',
    disputed: 'Origin uncertain', unfinished: 'Unfinished ancient Egyptian', replica: 'Modern replica'
  };
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const validPoint = stop => Number.isFinite(stop.lat) && Number.isFinite(stop.lon);
  const external = (url, title) => `<a href="${escape(url)}" target="_blank" rel="noopener noreferrer">${escape(title)} ↗</a>`;

  function renderVideos(record) {
    if (!record.videos?.length) return '';
    return `<section class="ob-videos" aria-labelledby="ob-videos-title">
      <h4 id="ob-videos-title">Watch</h4>
      <ul>${record.videos.map(video => {
        const url = new URL('https://www.youtube.com/watch');
        url.searchParams.set('v', video.id);
        if (video.start) url.searchParams.set('t', `${video.start}s`);
        return `<li>
          <a class="ob-video-link" href="${escape(url)}" target="_blank" rel="noopener noreferrer"
             data-atlas-video="${escape(video.id)}" data-title="${escape(video.title)}"
             data-creator="${escape(video.creator)}" data-start="${video.start || 0}">
            <span aria-hidden="true">▶</span><strong>${escape(video.label)}</strong>
          </a>
          <p>${escape(video.description)}</p>
          <small>${escape(video.creator)} · ${external(url, 'YouTube')}</small>
        </li>`;
      }).join('')}</ul>
    </section>`;
  }

  window.initAtlasObelisks = function(map, hooks = {}) {
    if (window.atlasObelisks) return window.atlasObelisks;
    let records, loading, selected, enabled = false, activeStep = -1, trigger, requestVersion = 0;
    let cluster, journeyLayer, groupPopup;
    const markers = new Map();
    const wrap = document.getElementById('map-wrap');
    const panel = document.createElement('section');
    panel.id = 'obelisk-panel';
    panel.hidden = true;
    panel.setAttribute('aria-label', 'Obelisk history and photographs');
    panel.innerHTML = '<div class="ob-panel-head"><div><p class="ob-eyebrow">Ancient Atlas · Map layer</p><h2>Obelisks</h2></div><button type="button" class="ob-close" aria-label="Hide Obelisks layer">×</button></div><div class="ob-panel-body"></div>';
    wrap.append(panel);
    const body = panel.querySelector('.ob-panel-body');
    const badge = document.createElement('div');
    badge.id = 'obelisk-map-control';
    badge.hidden = true;
    badge.innerHTML = '<button type="button" class="ob-browse">Obelisks · 29</button><button type="button" class="ob-hide" aria-label="Hide Obelisks layer">×</button>';
    wrap.append(badge);
    L.DomEvent.disableClickPropagation(panel);
    L.DomEvent.disableScrollPropagation(panel);
    L.DomEvent.disableClickPropagation(badge);

    const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
    const sidePanel = () => window.innerWidth > 950 || matchMedia('(orientation: landscape)').matches;
    function setURL(id) {
      const url = new URL(location.href);
      if (enabled) url.searchParams.set('obelisks', '1');
      else url.searchParams.delete('obelisks');
      if (id) {
        url.searchParams.set('obelisk', id);
        ['site','lidar','lidarSite'].forEach(key => url.searchParams.delete(key));
      } else url.searchParams.delete('obelisk');
      history.replaceState(history.state, '', url);
    }
    function syncButtons() {
      document.querySelectorAll('[data-obelisk-toggle]').forEach(button => {
        button.classList.toggle('on', enabled);
        button.setAttribute('aria-pressed', String(enabled));
      });
      badge.hidden = !enabled || !panel.hidden;
      document.body.classList.toggle('obelisks-enabled', enabled);
    }
    function openPanel() {
      panel.hidden = false;
      document.body.classList.add('obelisk-panel-open');
      syncButtons();
    }
    function closePanel({restoreFocus = false} = {}) {
      requestVersion++;
      if (groupPopup) {map.removeLayer(groupPopup);groupPopup=null;}
      panel.hidden = true;
      document.body.classList.remove('obelisk-panel-open');
      journeyLayer?.clearLayers();
      syncButtons();
      if (restoreFocus && trigger?.isConnected) trigger.focus({preventScroll:true});
    }
    function disable({restoreFocus = true, forgetSelection = false} = {}) {
      enabled = false;
      if (cluster) map.removeLayer(cluster);
      if (journeyLayer) map.removeLayer(journeyLayer);
      closePanel({restoreFocus});
      if (forgetSelection) selected = null;
      setURL();
      syncButtons();
    }
    function markerIcon(record, active = false) {
      return L.divIcon({
        className: `ob-marker ${record.category === 'replica' ? 'ob-marker-replica' : ''}${active ? ' ob-marker-selected' : ''}`,
        html: glyph, iconSize:[26,38], iconAnchor:[13,32], tooltipAnchor:[0,-26]
      });
    }
    // Group this small collection in screen space. The Atlas uses a changing,
    // fractional zoom floor; the general marker-cluster plugin can omit lone
    // markers at that floor. Keeping grouping local also preserves core sites.
    function drawMonuments() {
      if (!enabled || !cluster || !records) return;
      cluster.clearLayers();
      const groups=[];
      for (const record of records) {
        if (record.id===selected?.id) {cluster.addLayer(markers.get(record.id));continue;}
        const point=map.latLngToContainerPoint([record.lat,record.lon]);
        const nearby=groups.filter(group=>group.some(item=>point.distanceTo(item.point)<42));
        const group=[{record,point},...nearby.flat()];
        for (const match of nearby) groups.splice(groups.indexOf(match),1);
        groups.push(group);
      }
      for (const group of groups) {
        if (group.length===1) {cluster.addLayer(markers.get(group[0].record.id));continue;}
        const center=group.reduce((sum,item)=>sum.add(item.point),L.point(0,0)).divideBy(group.length);
        const point=map.containerPointToLatLng(center);
        const marker=L.marker(point,{
          icon:L.divIcon({className:'ob-cluster',html:`${glyph}<span>${group.length}</span>`,iconSize:[42,44]}),
          title:`${group.length} obelisks. Open this group.`,alt:`${group.length} obelisks`,zIndexOffset:900
        });
        marker.bindTooltip(escape(`${group.length} obelisks · open this group`));
        marker.on('click',()=>{
          if (map.getZoom()<16) {
            closePanel();
            map.fitBounds(group.map(item=>[item.record.lat,item.record.lon]),{padding:[60,60],maxZoom:17,animate:!reducedMotion()});
          } else {
            const list=document.createElement('div');list.className='ob-cluster-list';
            for (const item of group) {
              const button=document.createElement('button');button.type='button';button.textContent=item.record.name;
              button.addEventListener('click',()=>{map.closePopup();select(item.record.id,{fit:false,focus:true});});
              list.append(button);
            }
            L.DomEvent.disableClickPropagation(list);
            groupPopup=L.popup({className:'ob-popup'}).setLatLng(point).setContent(list).openOn(map);
          }
        });
        cluster.addLayer(marker);
      }
    }
    async function load() {
      if (records) return records;
      if (!loading) loading = fetch('/data/obelisks.json', {cache: 'no-cache'}).then(response => {
        if (!response.ok) throw new Error('The obelisk catalog could not load.');
        return response.json();
      }).then(data => {
        if (!Array.isArray(data) || !data.length) throw new Error('The obelisk catalog is empty.');
        records = data;
        map.createPane('obeliskJourneys');
        map.getPane('obeliskJourneys').style.zIndex = '450';
        journeyLayer = L.layerGroup();
        cluster = L.layerGroup();
        for (const record of records) {
          const marker = L.marker([record.lat,record.lon], {
            icon:markerIcon(record), title:record.name, alt:record.name, riseOnHover:true, zIndexOffset:700
          });
          marker.bindTooltip(escape(record.name));
          marker.on('click', () => select(record.id, {fit:false, focus:true}));
          markers.set(record.id, marker);
        }
        map.on('zoomend moveend resize',drawMonuments);
        return records;
      }).catch(error => { loading = null; throw error; });
      return loading;
    }
    function fitJourney() {
      const points = (selected?.journey || []).filter(validPoint).map(stop => [stop.lat,stop.lon]);
      if (!points.length) points.push([selected.lat,selected.lon]);
      const bounds = L.latLngBounds(points);
      map.invalidateSize();
      const size = map.getSize();
      const right = sidePanel() ? Math.min(panel.offsetWidth + 35, size.x * .5) : 30;
      const bottom = sidePanel() ? 35 : Math.min(panel.offsetHeight + 20, size.y * .62);
      map.fitBounds(bounds, {paddingTopLeft:[45,50], paddingBottomRight:[right,bottom], maxZoom:points.length>1?12:14, animate:!reducedMotion()});
    }
    function showStep(index, move = true) {
      activeStep = index;
      drawJourney();
      const stop = selected.journey[index];
      if (move && validPoint(stop)) {
        const zoom = index === selected.journey.length-1 ? 15 : 10;
        const container = map.getSize();
        const target = map.project([stop.lat,stop.lon],zoom);
        if (sidePanel()) target.x += panel.offsetWidth / 2;
        else target.y += Math.min(panel.offsetHeight/2,container.y*.29);
        map.setView(map.unproject(target,zoom),zoom,{animate:!reducedMotion()});
      }
      body.querySelectorAll('[data-ob-step]').forEach((button,i) => button.setAttribute('aria-pressed',String(i===index)));
    }
    function drawJourney() {
      journeyLayer.clearLayers();
      const steps = selected.journey || [];
      let previous;
      for (let index=0;index<steps.length;index++) {
        const stop = steps[index];
        if (!validPoint(stop)) {previous=null;continue;}
        const point = [stop.lat,stop.lon];
        if (previous) L.polyline([previous,point],{pane:'obeliskJourneys',color:'#d1ad60',weight:2,dashArray:'5 6',opacity:.85,interactive:false}).addTo(journeyLayer);
        previous=point;
        const active = index === activeStep;
        L.circleMarker(point,{pane:'obeliskJourneys',radius:active?8:5,color:active?'#fff3d3':'#d1ad60',fillColor:'#17171d',fillOpacity:1,weight:2})
          .bindTooltip(escape(`${stop.date} · ${stop.place}`))
          .on('click',()=>showStep(index,false)).addTo(journeyLayer);
      }
    }
    function render() {
      const record = selected;
      const photos = record.photos || [];
      const facts = [labels[record.category] || record.category,record.material];
      if (record.shaft_height_m) facts.push(`About ${record.shaft_height_m} m of stone`);
      const groups = [...new Set(records.map(item=>item.city))].sort((a,b)=>a.localeCompare(b));
      body.innerHTML = `<label class="ob-select-label" for="obelisk-select">Choose a monument</label>
        <select id="obelisk-select">${groups.map(city=>`<optgroup label="${escape(city)}">${records.filter(item=>item.city===city).map(item=>`<option value="${escape(item.id)}"${item.id===record.id?' selected':''}>${escape(item.name)}</option>`).join('')}</optgroup>`).join('')}</select>
        <article class="ob-dossier" data-obelisk-id="${escape(record.id)}">
          <p class="ob-eyebrow ob-current">${escape(record.city)} · ${escape(record.country)}</p>
          <h3 tabindex="-1">${escape(record.name)}</h3>
          <p class="ob-facts">${escape(facts.join(' · '))}</p>
          ${photos.map(photo=>`<figure class="ob-photo"><a href="${escape(photo.source_url)}" target="_blank" rel="noopener noreferrer" aria-label="Open photograph source for ${escape(record.name)}"><img src="${escape(photo.src)}" alt="${escape(photo.title || record.name)}" width="${photo.width||960}" height="${photo.height||1280}" decoding="async"></a><figcaption>${escape(photo.creator)} · ${external(photo.license_url,photo.license)} · ${external(photo.source_url,'Source')}</figcaption></figure>`).join('')}
          <p class="ob-summary">${escape(record.summary || record.notes)}</p>
          ${record.archival_photo ? `<p class="ob-archive">${external(record.archival_photo.url, record.archival_photo.title)}</p>` : ''}
          ${renderVideos(record)}
          <section class="ob-origin"><h4>${escape(record.origin_label || 'Original setting')}</h4><p><strong>${escape(record.original_site)}</strong></p><p>${escape(record.origin_note || '')}</p></section>
          <div class="ob-journey-heading"><h4>Journey milestones</h4><button type="button" data-ob-fit>Show whole journey</button></div>
          <ol class="ob-timeline">${(record.journey||[]).map((stop,index)=>`<li><button type="button" data-ob-step="${index}" aria-pressed="false"${!validPoint(stop)?' disabled':''}><span class="ob-date">${escape(stop.date)}</span><strong>${escape(stop.place)}</strong></button><p>${escape(stop.note)}</p></li>`).join('')}</ol>
          <p class="ob-map-note">Locations are approximate. Map lines connect known stops; they do not reconstruct the travel route.</p>
          <details class="ob-evidence"><summary>Measurements and historical sources</summary>${record.height_note?`<p>${escape(record.height_note)}</p>`:''}${record.mass_note?`<p>${escape(record.mass_note)}</p>`:''}<ul>${(record.sources||[]).map(source=>`<li>${external(source.url,source.title)}</li>`).join('')}</ul><p>Research checked ${escape(record.checked_date || '2026-11-18')}.</p></details>
          <a class="ob-share" href="/?obelisks=1&amp;obelisk=${encodeURIComponent(record.id)}">Link to this monument ↗</a>
        </article>`;
      body.querySelector('#obelisk-select').addEventListener('change',event=>{
        select(event.target.value,{fit:true,focus:false});
        body.querySelector('#obelisk-select').focus({preventScroll:true});
      });
      body.querySelector('[data-ob-fit]').addEventListener('click',()=>{
        activeStep=-1;drawJourney();fitJourney();
        body.querySelectorAll('[data-ob-step]').forEach(button=>button.setAttribute('aria-pressed','false'));
      });
      body.querySelectorAll('[data-ob-step]').forEach(button=>button.addEventListener('click',()=>showStep(Number(button.dataset.obStep))));
    }
    function select(id, {fit=true,focus=false} = {}) {
      if (!enabled) return;
      const record = records.find(item=>item.id===id);
      if (!record) return;
      hooks.prepareMap?.();
      for (const [key,marker] of markers) {
        marker.setIcon(markerIcon(records.find(item=>item.id===key),key===id));
        marker.setZIndexOffset(key===id?1400:700);
      }
      selected=record;
      activeStep=-1;
      openPanel();
      render();
      body.scrollTop=0;
      drawJourney();
      drawMonuments();
      if (fit) requestAnimationFrame(() => {
        if (enabled && !panel.hidden && selected === record) fitJourney();
      });
      setURL(id);
      if (focus) body.querySelector('h3').focus({preventScroll:true});
      window.atlasAnalytics?.('atlas_obelisk_view',id);
    }
    async function enable(id, source) {
      const version=++requestVersion;
      trigger=source || document.activeElement;
      enabled=true;
      hooks.prepareMap?.();
      openPanel();
      body.innerHTML='<p class="ob-loading" role="status">Opening the obelisk collection…</p>';
      try {
        await load();
        if (!enabled) return;
        cluster.addTo(map);journeyLayer.addTo(map);
        drawMonuments();
        badge.querySelector('.ob-browse').textContent=`Obelisks · ${records.length}`;
        if (version!==requestVersion) {syncButtons();return;}
        const requested=id || selected?.id || 'new-york';
        const initial=records.find(record=>record.id===requested) || records.find(record=>record.id==='new-york') || records[0];
        select(initial.id,{fit:true,focus:Boolean(source)});
        syncButtons();
      } catch(error) {
        if (!enabled || version!==requestVersion) return;
        body.innerHTML='<p role="alert">The obelisk collection could not open. Please try again.</p><button type="button" class="ob-retry">Try again</button>';
        body.querySelector('.ob-retry').addEventListener('click',()=>enable(id,source));
        console.warn(error);
      }
    }
    function renderToggle(container) {
      const button=document.createElement('button');
      button.type='button';
      button.className='net-toggle'+(enabled?' on':'');
      button.dataset.obeliskToggle='';
      button.setAttribute('aria-pressed',String(enabled));
      button.innerHTML=glyph+'Obelisks';
      button.addEventListener('click',()=>enabled?disable():enable(null,button));
      container.append(button);
    }
    panel.querySelector('.ob-close').addEventListener('click',disable);
    badge.querySelector('.ob-hide').addEventListener('click',disable);
    badge.querySelector('.ob-browse').addEventListener('click',()=>enable(selected?.id,badge.querySelector('.ob-browse')));
    document.querySelectorAll('[data-explore-obelisks]').forEach(button=>button.addEventListener('click',()=>enable(null,button)));
    document.addEventListener('keydown',event=>{
      if (event.key==='Escape' && !panel.hidden) {event.preventDefault();event.stopImmediatePropagation();closePanel({restoreFocus:true});}
    },true);
    window.addEventListener('resize',()=>{if (enabled && !panel.hidden) map.invalidateSize();});
    window.atlasObelisks={enable,disable,closePanel,renderToggle,get enabled(){return enabled;}};
    hooks.refreshControls?.();
    const params=new URLSearchParams(location.search);
    if (params.get('obelisks')==='1' || params.has('obelisk')) enable(params.get('obelisk'));
    return window.atlasObelisks;
  };
})();
