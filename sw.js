// Padel Techniekcoach: bewaart de app op het toestel (versie ae6a220fb208)
const CACHE = 'padelcoach-ae6a220fb208'
const BESTANDEN = [
  "./",
  "fonts.css",
  "fonts/barlow-condensed-latin-500-normal.woff2",
  "fonts/barlow-condensed-latin-600-normal.woff2",
  "fonts/barlow-condensed-latin-700-normal.woff2",
  "fonts/barlow-latin-400-normal.woff2",
  "fonts/barlow-latin-500-normal.woff2",
  "fonts/barlow-latin-600-normal.woff2",
  "fonts/barlow-latin-700-normal.woff2",
  "iconen/icoon-180.png",
  "iconen/icoon-192.png",
  "iconen/icoon-32.png",
  "iconen/icoon-512.png",
  "iconen/icoon-maskable-512.png",
  "index.html",
  "manifest.webmanifest",
  "vendor/react-dom.production.min.js",
  "vendor/react.production.min.js",
  "vendor/three.min.js"
]

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BESTANDEN)).then(() => self.skipWaiting()))
})

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((namen) => Promise.all(namen.filter((n) => n.startsWith('padelcoach-') && n !== CACHE).map((n) => caches.delete(n))))
      .then(() => self.clients.claim()),
  )
})

self.addEventListener('fetch', (e) => {
  const req = e.request
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return
  if (req.mode === 'navigate') {
    // de pagina zelf: eerst online (nieuwste versie), anders uit de bewaarde kopie
    e.respondWith(
      fetch(req)
        .then((res) => {
          const kopie = res.clone()
          caches.open(CACHE).then((c) => c.put('./', kopie))
          return res
        })
        .catch(() => caches.match('./')),
    )
    return
  }
  // de rest (bibliotheken, lettertypen, iconen): eerst uit de bewaarde kopie
  e.respondWith(caches.match(req).then((hit) => hit || fetch(req)))
})
