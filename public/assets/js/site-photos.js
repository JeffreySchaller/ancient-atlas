// Pure shared renderer. Site keys are canonical map names; metadata is escaped.
function photoEscape(value) { return String(value || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function renderSitePhotos(name) {
  const photos = typeof SITE_PHOTOS === 'undefined' ? [] : SITE_PHOTOS[name] || [];
  if (!photos.length) return '';
  return `<section class="site-photos" aria-label="Photographs of ${photoEscape(name)}"><div class="photo-heading">Photographs <span>${photos.length > 1 ? 'Scroll to explore →' : ''}</span></div><div class="photo-strip" tabindex="0" aria-label="Photo gallery">${photos.map(p => `<figure><a href="${photoEscape(p.source)}" target="_blank" rel="noopener" title="View original on Wikimedia Commons"><img src="${photoEscape(p.image)}" alt="${photoEscape(p.caption)}" width="${p.width}" height="${p.height}" loading="lazy" decoding="async"></a><figcaption><div>${photoEscape(p.caption)}</div><div class="photo-credit">${photoEscape(p.author)} · <a href="${photoEscape(p.license_url)}">${photoEscape(p.license)}</a> · <a href="${photoEscape(p.source)}">Commons ↗</a></div></figcaption></figure>`).join('')}</div></section>`;
}
