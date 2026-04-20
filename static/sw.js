// MediChain Service Worker
const CACHE_NAME = 'medichain-v1';
const STATIC_ASSETS = [
    '/',
    '/login',
    '/static/manifest.json',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Install - cache static assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(STATIC_ASSETS).catch(() => {});
        })
    );
    self.skipWaiting();
});

// Activate - clean old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

// ── SW message handler (from page) ───────────────────────────────────────
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SHOW_NOTIFICATION') {
        self.registration.showNotification(event.data.title, {
            body: event.data.body,
            icon: '/static/icons/icon-192.png',
            badge: '/static/icons/icon-192.png',
            vibrate: [200, 100, 200],
            tag: event.data.tag || 'medichain-reminder',
            renotify: true,
            data: { url: '/patient/reminders' }
        });
    }
});

// ── Push Notification handler ─────────────────────────────────────────────
self.addEventListener('push', event => {
    const data = event.data ? event.data.json() : {};
    const title = data.title || '💊 MediChain Reminder';
    const options = {
        body: data.body || 'Time to take your medicine!',
        icon: '/static/icons/icon-192.png',
        badge: '/static/icons/icon-192.png',
        vibrate: [200, 100, 200],
        tag: data.tag || 'medichain-reminder',
        renotify: true,
        data: { url: data.url || '/patient/reminders' }
    };
    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', event => {
    event.notification.close();
    const url = (event.notification.data && event.notification.data.url) || '/patient/reminders';
    event.waitUntil(clients.openWindow(url));
});

// ── Fetch - network first, fallback to cache ──────────────────────────────
self.addEventListener('fetch', event => {
    // Skip non-GET and API calls (always fresh)
    if (event.request.method !== 'GET') return;
    if (event.request.url.includes('/api/')) return;

    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Cache successful responses
                if (response && response.status === 200) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                }
                return response;
            })
            .catch(() => {
                // Offline fallback
                return caches.match(event.request).then(cached => {
                    if (cached) return cached;
                    // Offline page for navigation requests
                    if (event.request.mode === 'navigate') {
                        return new Response(`
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>MediChain - Offline</title>
                                <style>
                                    body { font-family: Arial, sans-serif; text-align: center; padding: 3rem; background: #f0f4ff; }
                                    .card { background: white; border-radius: 16px; padding: 2rem; max-width: 400px; margin: 0 auto; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
                                    h2 { color: #667eea; }
                                    p { color: #666; }
                                    button { background: #667eea; color: white; border: none; padding: 0.8rem 2rem; border-radius: 10px; font-size: 1rem; cursor: pointer; margin-top: 1rem; }
                                </style>
                            </head>
                            <body>
                                <div class="card">
                                    <div style="font-size:3rem;">📡</div>
                                    <h2>You are offline</h2>
                                    <p>MediChain requires an internet connection. Please check your network and try again.</p>
                                    <button onclick="window.location.reload()">Try Again</button>
                                </div>
                            </body>
                            </html>
                        `, { headers: { 'Content-Type': 'text/html' } });
                    }
                });
            })
    );
});
