const CACHE = 'fren-mobile-shell-v1';
const SHELL = ['./', './index.html', './styles.css', './app.js', './domain.js', './icon.svg', './icon-192.png', './icon-512.png', './manifest.webmanifest'];
self.addEventListener('install', event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL))));
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;
  const allowed = SHELL.map(path => new URL(path, self.registration.scope).href);
  if (!allowed.includes(url.href)) return;
  event.respondWith(fetch(event.request).catch(async () => {
    const cached = await caches.match(event.request, {cacheName: CACHE});
    return cached || Response.error();
  }));
});
