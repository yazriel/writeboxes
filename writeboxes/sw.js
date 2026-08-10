const CACHE_NAME = 'writeboxes-v1'
const ASSETS = [
  './',
  './index.html',
  './index.js',
  './style.css',
  './googleFilePickerServerAuth-2_WNVURq.js',
  './manifest.json',
  './icon/favicon-v4.ico',
  './icon/icon-192-v4.png',
  './icon/icon-512-v4.png',
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  )
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  )
  self.clients.claim()
})

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  )
})
