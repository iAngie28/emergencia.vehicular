self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    Promise.all([
      self.registration.unregister(),
      caches.keys().then((keys) =>
        Promise.all(
          keys
            .filter((key) => key.startsWith('ngsw:') || key.includes('ngsw'))
            .map((key) => caches.delete(key))
        )
      ),
      self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clients) =>
        Promise.all(clients.map((client) => client.navigate(client.url)))
      ),
    ])
  );
});
