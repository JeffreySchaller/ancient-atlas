(() => {
  'use strict';

  const bounds = [[51.391, -1.897], [51.448, -1.811]];
  const names = ['Avebury', 'Silbury Hill', 'West Kennet Long Barrow'];
  const terrainCredit = 'LiDAR DTM © <a href="https://www.data.gov.uk/dataset/01b3ee39-da3f-47b6-83da-dc98e73a461f/lidar-composite-digital-terrain-model-dtm-1m">Environment Agency</a> copyright and/or database right 2022';
  const imageryCredit = 'Imagery © <a href="https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9">Esri and its imagery contributors</a>';

  window.initAtlasLidarPilot = (map, sites) => {
    document.body.classList.add('lidar-pilot');
    const stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = '/assets/lidar/pilot.css';
    document.head.appendChild(stylesheet);

    const coverage = L.latLngBounds(bounds);
    const pilotSites = names.map(name => sites.find(site => site.n === name)).filter(Boolean);
    const siteBounds = L.latLngBounds(pilotSites.map(site => [site.lat, site.lng]));
    const imageryPane = map.createPane('lidar-pilot-imagery');
    imageryPane.style.zIndex = '380';
    const terrainPane = map.createPane('lidar-pilot-terrain');
    terrainPane.style.zIndex = '390';

    const southwest = map.options.crs.project(coverage.getSouthWest());
    const northeast = map.options.crs.project(coverage.getNorthEast());
    const imageWidth = 1200;
    const imageHeight = Math.round(imageWidth * (northeast.y - southwest.y) / (northeast.x - southwest.x));
    const imageryUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?' +
      new URLSearchParams({
        bbox: [southwest.x, southwest.y, northeast.x, northeast.y].join(','),
        bboxSR: '3857', imageSR: '3857', size: [imageWidth, imageHeight].join(','),
        format: 'jpg', f: 'image'
      });
    const imagery = L.imageOverlay(imageryUrl, coverage, {
      pane: 'lidar-pilot-imagery', attribution: imageryCredit, alt: 'Satellite imagery of the Avebury landscape'
    }).addTo(map);
    imagery.on('error', () => imagery.remove());

    const terrain = L.imageOverlay('/assets/lidar/avebury-hillshade.webp', coverage, {
      pane: 'lidar-pilot-terrain', attribution: terrainCredit, alt: 'Bare-earth hillshade from Environment Agency LiDAR'
    });

    const control = L.control({ position: 'topright' });
    control.onAdd = () => {
      const panel = L.DomUtil.create('section', 'lidar-pilot-panel');
      panel.setAttribute('aria-label', 'Avebury LiDAR pilot');
      panel.innerHTML = `
        <label class="lidar-pilot-toggle">
          <input type="checkbox" role="switch" id="lidar-pilot-toggle">
          <span>LiDAR hillshade</span>
        </label>
        <label class="lidar-pilot-opacity" for="lidar-pilot-opacity">
          Opacity <output for="lidar-pilot-opacity">65%</output>
        </label>
        <input type="range" id="lidar-pilot-opacity" min="0" max="100" value="65" disabled>
        <label class="lidar-pilot-site" for="lidar-pilot-site">Pilot site</label>
        <select id="lidar-pilot-site"><option value="">All three sites</option></select>
        <p class="lidar-pilot-status" role="status" hidden></p>
      `;
      L.DomEvent.disableClickPropagation(panel);
      L.DomEvent.disableScrollPropagation(panel);

      const toggle = panel.querySelector('#lidar-pilot-toggle');
      const slider = panel.querySelector('#lidar-pilot-opacity');
      const output = panel.querySelector('output');
      const picker = panel.querySelector('#lidar-pilot-site');
      const status = panel.querySelector('[role="status"]');
      for (const site of pilotSites) picker.add(new Option(site.n, site.n));

      function setOpacity() {
        terrain.setOpacity(Number(slider.value) / 100);
        output.value = slider.value + '%';
      }

      toggle.addEventListener('change', () => {
        status.hidden = true;
        slider.disabled = !toggle.checked;
        if (toggle.checked) terrain.addTo(map);
        else terrain.remove();
      });
      slider.addEventListener('input', setOpacity);
      terrain.on('error', () => {
        toggle.checked = false;
        slider.disabled = true;
        terrain.remove();
        status.textContent = 'LiDAR could not load. Turn it on to retry.';
        status.hidden = false;
      });

      picker.addEventListener('change', () => {
        const selected = pilotSites.find(site => site.n === picker.value);
        if (selected) map.setView([selected.lat, selected.lng], 16, { animate: false });
        else showOverview();
      });
      setOpacity();
      return panel;
    };

    function showOverview() {
      map.fitBounds(siteBounds, {
        paddingTopLeft: [45, 165], paddingBottomRight: [45, 70],
        maxZoom: 14.2, animate: false
      });
    }
    control.addTo(map);
    stylesheet.addEventListener('load', () => {
      map.invalidateSize({ pan: false });
      showOverview();
    }, { once: true });
    showOverview();
  };
})();
