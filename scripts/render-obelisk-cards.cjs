/* Run with Playwright and Chrome installed: node scripts/render-obelisk-cards.cjs */
const {chromium} = require('playwright');
const {mkdirSync, readFileSync} = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const publicDir = path.join(root, 'public');
const outputDir = path.join(publicDir, 'assets/social/obelisks');
const monuments = JSON.parse(readFileSync(path.join(root, 'data/obelisks.json'), 'utf8'));
const mapPage = readFileSync(path.join(publicDir, 'index.html'), 'utf8');
const logo = mapPage.match(/<div class="logo-box"[^>]*>\s*(<svg[\s\S]*?<\/svg>)/)?.[1];
const width = 1200;
const height = 630;
const photoArea = {width: 532, height: 552};
const locations = {
  'new-york': 'Central Park · New York City',
  'kingston-lacy': 'Kingston Lacy · Wimborne, Dorset',
  'senusret-heliopolis': 'Heliopolis · Cairo',
};

const escape = value => String(value).replace(/[&<>"']/g, char =>
  ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'})[char]);

function card(monument) {
  const photo = monument.photos[0];
  const photoBytes = readFileSync(path.join(publicDir, photo.src));
  const scale = Math.min(photoArea.width / photo.width, photoArea.height / photo.height);
  const [name] = monument.name.split(' — ');
  const location = locations[monument.id] || monument.city;
  const photographer = photo.creator.replace(/^Photograph by /, '').replace(/\s+\(www\.mikepeel\.net\)\.$/, '');

  return `<!doctype html><html lang="en">
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; }
  body { margin: 0; overflow: hidden; }
  main {
    position: relative;
    isolation: isolate;
    height: ${height}px;
    width: ${width}px;
    overflow: hidden;
    background: radial-gradient(ellipse at 71% 12%, #284748, #142d30 40%, #0a1c1e 85%);
    color: #fff7e9;
    font-family: Arial, sans-serif;
  }
  main::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset: auto 48% 0 0;
    height: 148px;
    background-image: linear-gradient(#bca06c 1px, transparent 1px), linear-gradient(90deg, #bca06c 1px, transparent 1px);
    background-size: 50px 50px;
    opacity: .13;
    mask-image: radial-gradient(ellipse at bottom left, #000 15%, transparent 69%);
  }
  .brand {
    position: absolute;
    left: 62px;
    top: 49px;
    display: flex;
    align-items: center;
    gap: 16px;
    font: 46px/1 Georgia, serif;
  }
  .brand svg { display: block; width: 62px; height: 62px; }
  .label {
    position: absolute;
    inset: 125px auto 110px 62px;
    width: 573px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  h1 {
    margin: 0;
    font: normal 95px/.99 Georgia, serif;
    letter-spacing: -.032em;
    text-wrap: balance;
  }
  .location {
    margin: 22px 0 0;
    color: #ead3a5;
    font-size: 36px;
    line-height: 1.17;
    letter-spacing: -.02em;
  }
  .photo {
    position: absolute;
    inset: 39px 35px auto auto;
    width: ${photoArea.width}px;
    height: ${photoArea.height}px;
    display: grid;
    place-items: center;
    margin: 0;
  }
  .photo img {
    display: block;
    box-shadow: 0 0 0 1px #edd2a237, 0 16px 34px #020c0e55;
  }
  .credit {
    position: absolute;
    left: 64px;
    bottom: 45px;
    width: 565px;
    margin: 0;
    color: #d7cdb6;
    font-size: 20px;
    line-height: 1.2;
  }
</style>
</head>
<body>
<main>
  <div class="brand">${logo}<span>Ancient Atlas</span></div>
  <div class="label">
    <h1>${escape(name)}</h1>
    <p class="location">${escape(location)}</p>
  </div>
  <figure class="photo">
    <img src="data:image/jpeg;base64,${photoBytes.toString('base64')}" alt=""
         width="${Math.round(photo.width * scale)}" height="${Math.round(photo.height * scale)}">
  </figure>
  <p class="credit">Photo: ${escape(photographer)} · ${escape(photo.license)}</p>
</main>
</body></html>`;
}

async function render() {
  if (!logo) throw new Error('The Atlas compass was not found in the map page.');
  mkdirSync(outputDir, {recursive: true});
  const browser = await chromium.launch({headless: true, channel: 'chrome'});
  try {
    const page = await browser.newPage({viewport: {width, height}, deviceScaleFactor: 1});
    for (const monument of monuments) {
      await page.setContent(card(monument));
      await page.locator('img').evaluate(img => img.decode());
      await page.evaluate(() => {
        const title = document.querySelector('h1');
        const label = document.querySelector('.label');
        const location = document.querySelector('.location');
        const available = label.clientHeight - location.offsetHeight - 22;
        let size = 95;
        while (title.offsetHeight > available || title.scrollWidth > title.clientWidth) {
          if (size <= 64) throw new Error(`Title is too long: ${title.textContent}`);
          size -= 1;
          title.style.fontSize = `${size}px`;
        }
      });
      await page.screenshot({path: path.join(outputDir, monument.id + '.jpg'), type: 'jpeg', quality: 91});
    }
  } finally {
    await browser.close();
  }
  console.log(`Rendered ${monuments.length} individual obelisk share cards.`);
}

render().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
