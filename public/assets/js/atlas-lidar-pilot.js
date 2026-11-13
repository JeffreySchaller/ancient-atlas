(() => {
  'use strict';

  const areas = [
    {
      bounds: [[51.391, -1.897], [51.448, -1.811]],
      terrain: 'avebury-hillshade.webp',
      names: ['Avebury', 'Silbury Hill', 'West Kennet Long Barrow']
    },
    {
      bounds: [[51.153, -1.878], [51.213, -1.742]],
      terrain: 'stonehenge-hillshade.webp',
      names: ['Stonehenge']
    }
  ];
  const terrainCredit = 'LiDAR DTM © <a href="https://www.data.gov.uk/dataset/01b3ee39-da3f-47b6-83da-dc98e73a461f/lidar-composite-digital-terrain-model-dtm-1m">Environment Agency</a> copyright and/or database right 2022';
  const imageryCredit = 'Imagery © <a href="https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9">Esri and its imagery contributors</a>';

  window.initAtlasLidarPilot = (map, sites) => {
    document.body.classList.add('lidar-pilot');
    const stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = '/assets/lidar/pilot.css';
    document.head.appendChild(stylesheet);

    const pilotSites = areas.flatMap(area => area.names.map(name => {
      const site = sites.find(candidate => candidate.n === name);
      return site && { ...site, area };
    }).filter(Boolean));
    const siteBounds = L.latLngBounds(pilotSites.filter(site => site.area === areas[0]).map(site => [site.lat, site.lng]));
    const imageryPane = map.createPane('lidar-pilot-imagery');
    imageryPane.style.zIndex = '380';
    const terrainPane = map.createPane('lidar-pilot-terrain');
    terrainPane.style.zIndex = '390';

    function createLayers(area) {
      const coverage = L.latLngBounds(area.bounds);
      const southwest = map.options.crs.project(coverage.getSouthWest());
      const northeast = map.options.crs.project(coverage.getNorthEast());
      const width = 1200;
      const height = Math.round(width * (northeast.y - southwest.y) / (northeast.x - southwest.x));
      const imageryUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?' +
        new URLSearchParams({
          bbox: [southwest.x, southwest.y, northeast.x, northeast.y].join(','),
          bboxSR: '3857', imageSR: '3857', size: [width, height].join(','),
          format: 'jpg', f: 'image'
        });
      const imagery = L.imageOverlay(imageryUrl, coverage, {
        pane: 'lidar-pilot-imagery', attribution: imageryCredit, alt: 'Satellite imagery of the selected landscape'
      });
      const terrain = L.imageOverlay('/assets/lidar/' + area.terrain, coverage, {
        pane: 'lidar-pilot-terrain', attribution: terrainCredit, alt: 'Bare-earth hillshade from Environment Agency LiDAR'
      });
      return { imagery, terrain };
    }

    const layers = new Map(areas.map(area => [area, createLayers(area)]));

    const requestedSite = new URLSearchParams(location.search).get('lidarSite');
    const control = L.control({ position: 'topright' });
    control.onAdd = () => {
      const panel = L.DomUtil.create('section', 'lidar-pilot-panel');
      panel.setAttribute('aria-label', 'LiDAR pilot');
      panel.innerHTML = `
        <div class="lidar-pilot-heading">
          <h2>Reveal the earthworks</h2>
          <a href="/" aria-label="Exit LiDAR comparison">Exit</a>
        </div>
        <label for="lidar-pilot-site">Explore a site</label>
        <select id="lidar-pilot-site"><option value="">Avebury area (three sites)</option></select>
        <label class="lidar-pilot-opacity" for="lidar-pilot-opacity">
          Drag to compare <output for="lidar-pilot-opacity">65% LiDAR</output>
        </label>
        <input type="range" id="lidar-pilot-opacity" min="0" max="100" value="65">
        <div class="lidar-pilot-endpoints" aria-hidden="true"><span>Satellite</span><span>LiDAR</span></div>
        <p class="lidar-pilot-status" role="status" hidden></p>
      `;
      L.DomEvent.disableClickPropagation(panel);
      L.DomEvent.disableScrollPropagation(panel);

      const slider = panel.querySelector('#lidar-pilot-opacity');
      const output = panel.querySelector('output');
      const picker = panel.querySelector('#lidar-pilot-site');
      const status = panel.querySelector('[role="status"]');
      for (const site of pilotSites) picker.add(new Option(site.n, site.n));

      picker.value = pilotSites.some(site => site.n === requestedSite) ? requestedSite : 'Stonehenge';
      const initialSite = pilotSites.find(site => site.n === picker.value);
      let activeLayers = layers.get(initialSite?.area ?? areas[0]);

      function setOpacity() {
        activeLayers.terrain.setOpacity(Number(slider.value) / 100);
        output.value = slider.value + '% LiDAR';
        slider.setAttribute('aria-valuetext', output.value);
      }

      slider.addEventListener('input', setOpacity);
      for (const entry of layers.values()) {
        entry.terrain.on('error', () => {
          if (entry !== activeLayers) return;
          slider.disabled = true;
          entry.terrain.remove();
          status.textContent = 'LiDAR couldn’t load. Reload the map to try again.';
          status.hidden = false;
        });
      }

      picker.addEventListener('change', () => {
        const selected = pilotSites.find(site => site.n === picker.value);
        const nextLayers = layers.get(selected?.area ?? areas[0]);
        if (nextLayers !== activeLayers) {
          activeLayers.imagery.remove();
          activeLayers.terrain.remove();
          activeLayers = nextLayers;
          activeLayers.imagery.addTo(map);
          status.hidden = true;
          slider.disabled = false;
          setOpacity();
          activeLayers.terrain.addTo(map);
        }
        if (selected) {
          const zoom = selected.n === 'Stonehenge' ? 14.8 : 16;
          map.setView([selected.lat, selected.lng], zoom, { animate: false });
        } else showOverview();
      });
      setOpacity();
      activeLayers.imagery.addTo(map);
      activeLayers.terrain.addTo(map);
      return panel;
    };

    function showOverview() {
      map.fitBounds(siteBounds, {
        paddingTopLeft: [45, 165], paddingBottomRight: [45, 70],
        maxZoom: 14.2, animate: false
      });
    }
    control.addTo(map);
    const picker = control.getContainer().querySelector('#lidar-pilot-site');
    function showInitialView() {
      map.invalidateSize({ pan: false });
      picker.dispatchEvent(new Event('change'));
    }
    stylesheet.addEventListener('load', showInitialView, { once: true });
    showInitialView();
  };
})();
