(() => {
  'use strict';

  const stages = {
    quarry: 'In quarry',
    moved: 'Transported',
    emplaced: 'Set in place'
  };
  const number = new Intl.NumberFormat('en-US', {maximumFractionDigits: 1});
  const tonnes = value => number.format(value) + ' t';
  const mass = stone => stone.mass_min_t === stone.mass_max_t
    ? tonnes(stone.mass_min_t)
    : number.format(stone.mass_min_t) + '–' + tonnes(stone.mass_max_t);
  const siteKey = stone => JSON.stringify([stone.site, stone.country]);

  window.initAtlasStoneWeights = function(map, hooks = {}) {
    if (window.atlasStoneWeights) return window.atlasStoneWeights;

    const layer = L.layerGroup();
    const panel = document.createElement('section');
    panel.id = 'stone-weight-panel';
    panel.hidden = true;
    panel.setAttribute('aria-labelledby', 'stone-weight-title');
    panel.innerHTML = `
      <div class="sw-head">
        <h2 id="stone-weight-title" tabindex="-1">Stone weights</h2>
        <button type="button" class="sw-close" aria-label="Close stone weights">×</button>
      </div>
      <div class="sw-body">
        <p class="sw-loading" role="status">Loading stone weights…</p>
        <div class="sw-error" hidden>
          <p role="alert">Stone weights couldn’t load.</p>
          <button type="button" class="sw-action sw-retry">Try again</button>
        </div>
        <div class="sw-controls" hidden>
          <p class="sw-intro">Compare individual stones by estimated weight.</p>
          <div class="sw-range-label">
            <label for="stone-weight-minimum">Minimum weight</label>
            <output for="stone-weight-minimum">All weights</output>
          </div>
          <input id="stone-weight-minimum" type="range" min="0" step="25" value="0" aria-describedby="stone-weight-method">
          <p id="stone-weight-method" class="sw-note">Weights use metric tonnes. A range qualifies when its lower estimate meets the minimum.</p>
          <label class="sw-label" for="stone-weight-status">What happened to the stone?</label>
          <select id="stone-weight-status">
            <option value="all">All stones</option>
            <option value="transported">Transported</option>
            <option value="quarry">In quarry</option>
          </select>
          <div class="sw-results-bar">
            <p id="stone-weight-count" role="status" aria-atomic="true"></p>
            <button type="button" class="sw-action sw-fit">Fit results</button>
          </div>
          <div class="sw-results">
            <label class="sw-label" for="stone-weight-select">Choose a stone</label>
            <select id="stone-weight-select"></select>
            <article class="sw-record">
              <p class="sw-location"></p>
              <h3 tabindex="-1"></h3>
              <div class="sw-measure">
                <span class="sw-estimate"><strong></strong><small hidden></small></span>
                <span class="sw-stage"></span>
              </div>
              <p class="sw-record-note"></p>
              <a class="sw-source" target="_blank" rel="noopener noreferrer"></a>
            </article>
            <ul class="sw-legend" aria-label="Map pin legend">
              <li><span class="sw-key sw-emplaced" aria-hidden="true"></span>Set in place</li>
              <li><span class="sw-key sw-moved" aria-hidden="true"></span>Transported</li>
              <li><span class="sw-key sw-quarry" aria-hidden="true"></span>In quarry</li>
            </ul>
          </div>
        </div>
        <a class="sw-experience" href="/experiences/feel-the-weight/">
          <strong>Feel the Weight →</strong>
          <span>Get a sense of how heavy one stone is.</span>
        </a>
      </div>`;
    document.getElementById('map-wrap').append(panel);
    L.DomEvent.disableClickPropagation(panel);
    L.DomEvent.disableScrollPropagation(panel);
    const title = panel.querySelector('h2');
    const loading = panel.querySelector('.sw-loading');
    const error = panel.querySelector('.sw-error');
    const controls = panel.querySelector('.sw-controls');
    const resultCount = panel.querySelector('#stone-weight-count');
    const slider = panel.querySelector('#stone-weight-minimum');
    const output = panel.querySelector('output');
    const status = panel.querySelector('#stone-weight-status');
    const select = panel.querySelector('#stone-weight-select');
    const results = panel.querySelector('.sw-results');
    const fit = panel.querySelector('.sw-fit');
    const record = panel.querySelector('.sw-record');
    const locationLabel = record.querySelector('.sw-location');
    const name = record.querySelector('h3');
    const estimate = record.querySelector('.sw-estimate strong');
    const qualifier = record.querySelector('.sw-estimate small');
    const stage = record.querySelector('.sw-stage');
    const note = record.querySelector('.sw-record-note');
    const source = record.querySelector('.sw-source');
    const markers = new Map();
    let enabled = false;
    let trigger, pending, catalog;
    let visible = [];
    let visibleSites = new Map();
    let selected = null;
    let version = 0;

    function loadCatalog() {
      pending ??= fetch('/data/stone-weights.json').then(response => {
        if (!response.ok) throw new Error('Stone catalog unavailable');
        return response.json();
      }).then(data => {
        if (!Array.isArray(data) || !data.length) throw new Error('Empty stone catalog');
        return data.sort((first, second) => second.mass_min_t - first.mass_min_t);
      }).catch(cause => {
        pending = null;
        throw cause;
      });
      return pending;
    }

    function sidePanel() {
      return window.innerWidth > 950 || matchMedia('(orientation: landscape)').matches;
    }

    function fitStones(stones) {
      if (!stones.length) return;
      const size = map.getSize();
      const right = sidePanel() ? Math.min(panel.offsetWidth + 20, size.x * .55) : 25;
      const bottom = sidePanel() ? 25 : Math.min(panel.offsetHeight + 20, size.y * .63);
      map.fitBounds(stones.map(stone => [stone.lat, stone.lng]), {
        paddingTopLeft: [25, 65],
        paddingBottomRight: [right, bottom],
        maxZoom: stones.length === 1 ? 12 : 8,
        animate: !matchMedia('(prefers-reduced-motion: reduce)').matches
      });
    }

    function showStone(stone, focus = false) {
      selected = stone;
      record.hidden = !stone;
      if (!stone) return;
      select.value = stone.id;
      locationLabel.textContent = [stone.site, stone.country].filter(Boolean).join(' · ');
      name.textContent = stone.name;
      estimate.textContent = mass(stone);
      qualifier.textContent = stone.mass_qualifier || '';
      qualifier.hidden = !stone.mass_qualifier;
      stage.textContent = stages[stone.status];
      stage.className = 'sw-stage sw-' + stone.status;
      note.textContent = stone.note;
      source.href = stone.source_url;
      source.textContent = stone.source_title + ' ↗';
      highlightPin();
      if (focus) name.focus();
    }

    function highlightPin() {
      const key = selected && siteKey(selected);
      for (const {marker, sites} of markers.values()) {
        marker.getElement()?.classList.toggle('sw-pin-active', sites.includes(key));
      }
    }

    function drawPins() {
      if (!enabled) return;
      layer.clearLayers();
      markers.clear();

      // Nearby sites share a clickable pin until they separate on zoom.
      const groups = [];
      for (const [key, stones] of visibleSites) {
        const point = map.latLngToContainerPoint([stones[0].lat, stones[0].lng]);
        const group = groups.find(candidate => candidate.point.distanceTo(point) < 32);
        if (group) {
          group.sites.push(key);
          group.stones.push(...stones);
        } else {
          groups.push({point, sites: [key], stones: [...stones]});
        }
      }

      for (const {point, sites, stones} of groups) {
        const first = stones[0];
        const grouped = stones.length > 1;
        const count = stones.length + ' stones';
        const label = !grouped ? first.name + ' · ' + mass(first)
          : sites.length === 1 ? first.site + ' · ' + count
          : count + ' at ' + sites.length + ' nearby sites';
        const tooltip = document.createElement('span');
        tooltip.textContent = label;
        const icon = L.divIcon({
          className: grouped ? 'sw-pin sw-pin-group' : 'sw-pin sw-' + first.status,
          html: grouped ? String(stones.length) : '<span aria-hidden="true"></span>',
          iconSize: [30, 30],
          iconAnchor: [15, 15],
          tooltipAnchor: [0, -14]
        });
        const marker = L.marker(map.containerPointToLatLng(point), {icon, title: label, riseOnHover: true, zIndexOffset: 750});
        marker.bindTooltip(tooltip);
        if (grouped) {
          const list = document.createElement('div');
          list.className = 'sw-site-choices';
          for (const stone of stones) {
            const button = document.createElement('button');
            button.type = 'button';
            button.textContent = stone.name + ' · ' + mass(stone);
            button.addEventListener('click', () => {
              marker.closePopup();
              showStone(stone, true);
            });
            list.append(button);
          }
          marker.bindPopup(list, {className: 'sw-site-popup'});
          marker.on('popupopen', () => list.firstElementChild.focus({preventScroll: true}));
        } else {
          marker.on('click', () => showStone(first, true));
        }
        layer.addLayer(marker);
        marker.getElement()?.setAttribute('aria-label', label);
        markers.set(sites[0], {marker, sites});
      }
      highlightPin();
    }

    function applyFilters() {
      const cutoff = Number(slider.value);
      const filter = status.value;
      output.textContent = cutoff ? tonnes(cutoff) : 'All weights';
      slider.setAttribute('aria-valuetext', cutoff ? 'At least ' + number.format(cutoff) + ' metric tonnes' : 'All weights');
      visible = catalog.filter(stone => stone.mass_min_t >= cutoff && (
        filter === 'all' || (filter === 'transported' ? stone.status !== 'quarry' : stone.status === 'quarry')
      ));

      const bySite = new Map();
      for (const stone of visible) {
        const key = siteKey(stone);
        if (!bySite.has(key)) bySite.set(key, []);
        bySite.get(key).push(stone);
      }
      resultCount.textContent = visible.length
        ? `${visible.length} ${visible.length === 1 ? 'stone' : 'stones'} at ${bySite.size} ${bySite.size === 1 ? 'site' : 'sites'}`
        : 'No stones match these filters.';
      results.hidden = !visible.length;
      fit.disabled = !visible.length;
      select.replaceChildren(...visible.map(stone => new Option(stone.name + ' · ' + mass(stone), stone.id)));
      visibleSites = bySite;
      drawPins();
      showStone(visible.find(stone => stone.id === selected?.id) || visible[0]);
    }

    async function open(from) {
      if (!enabled) {
        trigger = from;
        hooks.prepareMap?.();
        enabled = true;
        document.body.classList.add('stone-weights-enabled');
        panel.hidden = false;
        layer.addTo(map);
        if (from) title.focus({preventScroll: true});
      }
      const request = ++version;
      error.hidden = true;
      if (!catalog) loading.hidden = false;
      try {
        const data = await loadCatalog();
        if (!enabled || request !== version) return;
        catalog = data;
        slider.max = String(Math.max(1000, Math.ceil(catalog[0].mass_min_t / 25) * 25 + 25));
        controls.hidden = false;
        loading.hidden = true;
        applyFilters();
        map.invalidateSize({pan: false});
        fitStones(visible);
      } catch {
        if (!enabled || request !== version) return;
        loading.hidden = true;
        error.hidden = false;
      }
    }

    function close({restoreFocus = true, restoreMap = true} = {}) {
      if (!enabled) return;
      enabled = false;
      version++;
      panel.hidden = true;
      layer.clearLayers();
      markers.clear();
      layer.remove();
      map.stop();
      document.body.classList.remove('stone-weights-enabled');
      if (restoreMap) hooks.restoreMap?.();
      if (restoreFocus && trigger?.getClientRects().length) trigger.focus({preventScroll: true});
    }

    panel.querySelector('.sw-close').addEventListener('click', () => close());
    panel.querySelector('.sw-retry').addEventListener('click', () => open());
    slider.addEventListener('input', applyFilters);
    status.addEventListener('change', applyFilters);
    fit.addEventListener('click', () => fitStones(visible));
    select.addEventListener('change', () => {
      const stone = visible.find(item => item.id === select.value);
      if (!stone) return;
      showStone(stone);
      fitStones([stone]);
    });
    document.addEventListener('keydown', event => {
      if (enabled && event.key === 'Escape') {
        event.preventDefault();
        event.stopImmediatePropagation();
        close();
      }
    }, true);
    map.on('zoomend resize', drawPins);
    window.atlasStoneWeights = {open, close, get enabled() { return enabled; }};
    return window.atlasStoneWeights;
  };
})();
