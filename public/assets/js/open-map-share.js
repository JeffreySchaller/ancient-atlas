(() => {
  const link = document.querySelector('[data-open-atlas-map]');
  const destination = new URL(link.href);
  const incoming = new URLSearchParams(location.search);
  const filter = link.dataset.mapShareParam;
  if (filter && incoming.has(filter)) destination.searchParams.set(filter, incoming.get(filter));
  for (const [key, value] of incoming) {
    if (key.startsWith('utm_') || ['gclid', 'gbraid', 'wbraid'].includes(key)) {
      destination.searchParams.set(key, value);
    }
  }
  location.replace(destination.href);
})();
