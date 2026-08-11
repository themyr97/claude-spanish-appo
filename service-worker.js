// Bump APP_VERSION on every deploy — this changes the SW file itself,
// which is what triggers browsers to install a fresh worker and purge old caches.
const APP_VERSION = 'v13';
const CACHE_NAME = 'espanol-app-' + APP_VERSION;

const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('message', event => {
  if(event.data === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', event => {
  const req = event.request;

  // NETWORK-FIRST for navigations and HTML: always try to get the newest app shell,
  // fall back to cache only when offline. This is what makes updates actually arrive.
  const isHTML = req.mode === 'navigate' ||
                 (req.headers.get('accept') || '').includes('text/html');

  if(isHTML){
    event.respondWith(
      fetch(req)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put('./index.html', clone));
          return response;
        })
        .catch(() => caches.match('./index.html').then(c => c || caches.match('./')))
    );
    return;
  }

  // STALE-WHILE-REVALIDATE for other same-origin assets: serve fast from cache,
  // but refresh the copy in the background so the next launch is current.
  if(req.url.startsWith(self.location.origin)){
    event.respondWith(
      caches.match(req).then(cached => {
        const network = fetch(req).then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, clone));
          return response;
        }).catch(() => cached);
        return cached || network;
      })
    );
    return;
  }

  // Cross-origin (e.g. Google Fonts): network with cache fallback.
  event.respondWith(fetch(req).catch(() => caches.match(req)));
});
