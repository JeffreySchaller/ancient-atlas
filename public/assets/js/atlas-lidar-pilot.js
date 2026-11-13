(() => {
  'use strict';

  const areas = [
    {
      bounds: [[51.391, -1.897], [51.448, -1.811]],
      terrain: 'avebury-hillshade.webp'
    },
    {
      bounds: [[51.153, -1.878], [51.213, -1.742]],
      terrain: 'stonehenge-hillshade.webp'
    }
  ];
  const terrainCredit = 'LiDAR DTM © <a href="https://www.data.gov.uk/dataset/01b3ee39-da3f-47b6-83da-dc98e73a461f/lidar-composite-digital-terrain-model-dtm-1m">Environment Agency</a> copyright and/or database right 2022';
  const imageryCredit = 'Imagery © <a href="https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9">Esri and its imagery contributors</a>';

  let activate;
  let closeComparison;
  let lastSite;
  const coverageFor = point => areas.find(area => L.latLngBounds(area.bounds).contains(point));

  window.watchAtlasLidarCoverage = (map, { getSite, sites, open }) => {
    const button = document.getElementById('lidar-map-button');
    const announced = new Set();
    let destination;

    function refresh() {
      const view = map.getBounds();
      const center = map.getCenter();
      const site = getSite() || lastSite;
      const preferred = site && coverageFor([site.lat, site.lng]);
      const visible = areas.filter(area => {
        const bounds = L.latLngBounds(area.bounds);
        const size = map.project(bounds.getNorthEast()).subtract(map.project(bounds.getSouthWest()));
        return view.overlaps(bounds) && Math.min(Math.abs(size.x), Math.abs(size.y)) >= 32;
      });
      const area = visible.includes(preferred) ? preferred :
        visible.find(candidate => L.latLngBounds(candidate.bounds).contains(center)) ?? visible[0];
      const active = document.body.classList.contains('lidar-pilot');
      destination = area && (area === preferred ? site : sites.find(candidate => coverageFor([candidate.lat, candidate.lng]) === area));
      button.hidden = !active && !destination;
      button.setAttribute('aria-expanded', String(active));
      button.setAttribute('aria-label', active ? 'Close LiDAR comparison' : 'LiDAR available here');
      if (!active && area && destination && !announced.has(area)) {
        announced.add(area);
        button.classList.remove('lidar-available-cue');
        void button.offsetWidth;
        button.classList.add('lidar-available-cue');
      }
    }

    L.DomEvent.disableClickPropagation(button);
    button.addEventListener('click', () => {
      if (document.body.classList.contains('lidar-pilot')) closeComparison();
      else if (destination) open(destination.n);
    });
    map.on('moveend resize lidarstatechange', refresh);
    refresh();
  };

  window.initAtlasLidarPilot = (map, { site, openSite, keepView }) => {
    if (activate) {
      activate(site, true, keepView);
      return;
    }

    const stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = '/assets/lidar/pilot.css';
    document.head.appendChild(stylesheet);

    const imageryPane = map.createPane('lidar-pilot-imagery');
    imageryPane.style.zIndex = '380';
    const terrainPane = map.createPane('lidar-pilot-terrain');
    terrainPane.style.zIndex = '390';
    const imagery = L.layerGroup(areas.map(area => {
      const bounds = L.latLngBounds(area.bounds);
      const sw = map.options.crs.project(bounds.getSouthWest());
      const ne = map.options.crs.project(bounds.getNorthEast());
      const width = 1200;
      const height = Math.round(width * (ne.y - sw.y) / (ne.x - sw.x));
      const params = new URLSearchParams({
        bbox: [sw.x, sw.y, ne.x, ne.y].join(','),
        bboxSR: '3857',
        imageSR: '3857',
        size: [width, height].join(','),
        format: 'jpg',
        f: 'image'
      });
      return L.imageOverlay(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?' + params,
        bounds, { pane: 'lidar-pilot-imagery', attribution: imageryCredit, alt: 'Satellite imagery within the LiDAR survey' }
      );
    }));
    const terrain = L.layerGroup(areas.map(area => L.imageOverlay(
      '/assets/lidar/' + area.terrain, area.bounds,
      { pane: 'lidar-pilot-terrain', attribution: terrainCredit, alt: 'Bare-earth LiDAR hillshade' }
    )));

    const control = L.control({ position: 'topright' });
    control.onAdd = () => {
      const panel = L.DomUtil.create('section', 'lidar-pilot-panel');
      panel.setAttribute('aria-label', 'LiDAR comparison');
      panel.innerHTML = `
        <div class="lidar-pilot-blend">
          <input type="range" id="lidar-pilot-opacity" min="0" max="100" value="65"
            aria-label="Satellite to LiDAR blend">
          <div class="lidar-pilot-endpoints" aria-hidden="true"><span>Satellite</span><span>LiDAR</span></div>
        </div>
        <button class="lidar-pilot-close" type="button" aria-label="Close LiDAR comparison">×</button>
        <p class="lidar-pilot-status" role="status" hidden></p>
      `;
      L.DomEvent.disableClickPropagation(panel);
      L.DomEvent.disableScrollPropagation(panel);

      const slider = panel.querySelector('#lidar-pilot-opacity');
      const status = panel.querySelector('[role="status"]');

      function setOpacity() {
        terrain.eachLayer(layer => layer.setOpacity(Number(slider.value) / 100));
        slider.setAttribute('aria-valuetext', slider.value + '% LiDAR');
      }

      slider.addEventListener('input', setOpacity);
      terrain.eachLayer(layer => layer.on('error', () => {
        status.textContent = 'Some LiDAR imagery couldn’t load.';
        status.hidden = false;
      }));
      let activeArea;
      let introduced = false;
      closeComparison = () => {
        imagery.remove();
        terrain.remove();
        panel.hidden = true;
        panel.classList.remove("lidar-intro");
        activeArea = undefined;
        document.querySelectorAll('.lidar-directory [aria-current]').forEach(link => link.removeAttribute('aria-current'));
        document.body.classList.remove('lidar-pilot');
        const url = new window.URL(location.href);
        url.searchParams.delete('lidar');
        url.searchParams.delete('lidarSite');
        history.replaceState(history.state, '', url);
        map.invalidateSize({ pan: false });
        map.fire('lidarstatechange');
        const button = document.getElementById('lidar-map-button');
        const nextFocus = button.hidden ? document.querySelector('#detail .lidar-discovery') : button;
        nextFocus?.focus({ preventScroll: true });
      };
      panel.querySelector('button').addEventListener('click', closeComparison);

      activate = (nextSite, animate, preserveView) => {
        lastSite = nextSite;
        document.body.classList.add('lidar-pilot', 'lidar-map-open');
        panel.hidden = false;
        if (!introduced) {
          panel.classList.add('lidar-intro');
          introduced = true;
        }
        openSite(nextSite);
        document.querySelectorAll('.lidar-directory a[data-lidar-site]').forEach(link => {
          const current = link.dataset.lidarSite === nextSite.n &&
            (!link.classList.contains('lidar-landscape-link') || !link.parentElement.querySelector('ul'));
          if (current) link.setAttribute('aria-current', 'true');
          else link.removeAttribute('aria-current');
        });
        const point = [nextSite.lat, nextSite.lng];
        const area = coverageFor(point);
        if (area && activeArea === area) return;
        activeArea = area;
        map.stop();
        setOpacity();
        imagery.addTo(map);
        terrain.addTo(map);
        map.invalidateSize({ pan: false });
        map.fire('lidarstatechange');
        if (preserveView) return;
        const coverage = area && L.latLngBounds(area.bounds);
        const center = coverage ? coverage.getCenter() : point;
        // Leave roughly a third of the limiting dimension for satellite context.
        const zoom = coverage ? map.getBoundsZoom(coverage, false, map.getSize().multiplyBy(0.35)) : 13;
        if (animate && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
          map.flyTo(center, zoom, { duration: 1.25 });
        } else {
          map.setView(center, zoom, { animate: false });
        }
      };
      return panel;
    };
    control.addTo(map);
    // Wait for the split map and walkthrough layout before flying.
    stylesheet.addEventListener('load', () => activate(site, true, keepView), { once: true });
    stylesheet.addEventListener('error', () => activate(site, false, keepView), { once: true });
  };
})();
