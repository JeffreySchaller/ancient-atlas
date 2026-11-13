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

  window.initAtlasLidarPilot = (map, { site, openSite }) => {
    if (activate) {
      activate(site, true);
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
    const imagery = L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      { pane: 'lidar-pilot-imagery', attribution: imageryCredit, maxNativeZoom: 18, noWrap: true }
    );
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
      panel.querySelector('button').addEventListener('click', () => {
        imagery.remove();
        terrain.remove();
        panel.hidden = true;
        activeArea = undefined;
        document.querySelectorAll('.lidar-directory [aria-current]').forEach(link => link.removeAttribute('aria-current'));
        document.body.classList.remove('lidar-pilot');
        const url = new window.URL(location.href);
        url.searchParams.delete('lidar');
        url.searchParams.delete('lidarSite');
        history.replaceState(history.state, '', url);
        map.invalidateSize({ pan: false });
        document.querySelector('#detail .lidar-discovery')?.focus({ preventScroll: true });
      });

      activate = (nextSite, animate) => {
        document.body.classList.add('lidar-pilot');
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
        const area = areas.find(candidate => L.latLngBounds(candidate.bounds).contains(point));
        if (area && activeArea === area) return;
        activeArea = area;
        map.stop();
        setOpacity();
        imagery.addTo(map);
        terrain.addTo(map);
        map.invalidateSize({ pan: false });
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
    stylesheet.addEventListener('load', () => activate(site, true), { once: true });
    stylesheet.addEventListener('error', () => activate(site, false), { once: true });
  };
})();
