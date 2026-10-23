// GA4 is optional. GoatCounter remains independent and is not changed here.
(() => {
  if (!['theancientatlas.com', 'www.theancientatlas.com'].includes(location.hostname)) return;
  const id = 'G-LZSJ94PNP6';
  const key = 'atlas-analytics-v1';
  const blocked = navigator.globalPrivacyControl === true;
  let consent = null;
  try { consent = localStorage.getItem(key); } catch (_) { /* Page-local choice. */ }
  if (blocked) consent = 'denied';
  let started = false;
  const gtag = function () { window.dataLayer.push(arguments); };
  function start() {
    if (started || consent !== 'granted') return;
    started = true;
    window.dataLayer = window.dataLayer || [];
    gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
    gtag('consent', 'update', { analytics_storage: 'granted' });
    gtag('js', new Date());
    const clean = new URL(location.pathname, location.origin);
    const params = new URLSearchParams(location.search);
    for (const name of ['utm_source', 'utm_medium', 'utm_campaign', 'gclid', 'gbraid', 'wbraid']) {
      if (params.has(name)) clean.searchParams.set(name, params.get(name));
    }
    let referrer = '';
    try { referrer = document.referrer ? new URL(document.referrer).origin + '/' : ''; } catch (_) { /* Invalid referrer. */ }
    gtag('config', id, { page_location: clean.href, page_referrer: referrer, allow_google_signals: false, allow_ad_personalization_signals: false });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(script);
  }
  // Called only with names from the Atlas catalog or valid YouTube video IDs.
  window.atlasAnalytics = (event, value) => {
    if (!started || consent !== 'granted') return;
    if (event === 'atlas_site_view' && typeof value === 'string') {
      gtag('event', event, { send_to: id, site_name: value.slice(0, 100) });
    } else if (event === 'atlas_video_open' && /^[A-Za-z0-9_-]{11}$/.test(value)) {
      gtag('event', event, { send_to: id, video_id: value });
    }
  };
  const style = document.createElement('style');
  style.textContent = '#atlas-analytics-panel{position:fixed;bottom:12px;left:12px;right:12px;margin:0 auto;max-width:680px;max-height:65vh;overflow:auto;z-index:10020;background:#15151c;color:#f0eee9;border:1px solid #8a6e2f;border-radius:10px;padding:18px;box-shadow:0 8px 30px #0008;font:14px/1.5 system-ui,sans-serif}#atlas-analytics-panel[hidden]{display:none}#atlas-analytics-panel p{margin:0 0 12px}#atlas-analytics-panel a{color:#f0d69b}#atlas-analytics-panel button{font:inherit;padding:9px 14px;border:1px solid #8a6e2f;border-radius:5px;background:#15151c;color:#f0eee9;cursor:pointer;margin:0 8px 0 0}#atlas-analytics-panel button:focus-visible,#atlas-analytics-settings:focus-visible{outline:2px solid #f0d69b;outline-offset:3px}#atlas-analytics-panel button[data-choice="granted"]{background:#c9a84c;color:#15151c}#atlas-analytics-settings{position:fixed;bottom:8px;right:8px;z-index:10010;background:#15151c;color:#f0eee9;border:1px solid #8a6e2f;border-radius:5px;padding:6px 9px;font:12px/1.3 system-ui,sans-serif;cursor:pointer}';
  document.head.appendChild(style);
  const settings = document.createElement('button');
  settings.id = 'atlas-analytics-settings';
  settings.type = 'button';
  settings.textContent = 'Analytics preferences';
  const panel = document.createElement('section');
  panel.id = 'atlas-analytics-panel';
  panel.hidden = true;
  panel.setAttribute('aria-label', 'Analytics preferences');
  panel.innerHTML = '<p><strong>Help us understand how people explore the Atlas.</strong> May we use Google Analytics cookies to measure visits, site exploration, and video clicks? If you allow this, that activity is shared with Google and reports are linked to our Google Ads account. Personalized advertising is off. GoatCounter continues to provide separate visitor statistics. <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google uses this information</a>. You can change your choice in Analytics preferences.</p><div><button type="button" data-choice="granted">Allow analytics</button><button type="button" data-choice="denied">No thanks</button></div>';
  if (blocked) {
    panel.querySelector('p').textContent = 'Your browser’s Global Privacy Control is enabled, so Google Analytics is off. GoatCounter continues to provide separate visitor statistics.';
    panel.querySelector('[data-choice="granted"]').hidden = true;
    panel.querySelector('[data-choice="denied"]').textContent = 'Close';
  }
  settings.addEventListener('click', () => { panel.hidden = false; panel.querySelector(blocked ? '[data-choice="denied"]' : 'button').focus(); });
  panel.querySelectorAll('[data-choice]').forEach(button => button.addEventListener('click', () => {
    consent = blocked ? 'denied' : button.dataset.choice;
    try { localStorage.setItem(key, consent); } catch (_) { /* Page-local choice. */ }
    panel.hidden = true;
    if (consent === 'granted') start();
    else if (started) {
      gtag('consent', 'update', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
      location.reload();
    }
    settings.focus();
  }));
  document.body.appendChild(settings);
  document.body.appendChild(panel);
  if (consent === 'granted') start();
  else if (!consent) panel.hidden = false;
})();
