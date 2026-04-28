// firebase-messaging-sw.js
// Este es el Service Worker para manejar notificaciones Firebase en segundo plano

importScripts('https://www.gstatic.com/firebasejs/10.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.0.0/firebase-messaging-compat.js');

// Inicializar Firebase con la configuración web
firebase.initializeApp({
  apiKey: "AIzaSyAN4sQc58P6fwKWKVjM6kVhSCEBbEqR3mQ",
  authDomain: "emergenciavehicular.firebaseapp.com",
  projectId: "emergenciavehicular",
  storageBucket: "emergenciavehicular.firebasestorage.app",
  messagingSenderId: "707296553697",
  appId: "1:707296553697:web:4f755c896153596308e5a0"
});

const messaging = firebase.messaging();

// Manejador de notificaciones en segundo plano
messaging.onBackgroundMessage((payload) => {
  console.log('🔔 Notificación recibida en segundo plano:', payload);

  const notificationTitle = payload.notification.title || '🚨 Incidente Cercano';
  const notificationOptions = {
    body: payload.notification.body || 'Nuevo incidente reportado',
    icon: '/assets/icon-192x192.png',
    badge: '/assets/badge-72x72.png',
    data: payload.data || {},
    tag: 'incidente-' + (payload.data?.id || new Date().getTime()),
    requireInteraction: true // No desaparece automáticamente
  };

  return self.registration.showNotification(notificationTitle, notificationOptions);
});

// Manejador de clicks en notificaciones
self.addEventListener('notificationclick', function(event) {
  console.log('👆 Notificación clickeada:', event.notification.tag);
  
  const notification = event.notification;
  const incidenteId = notification.data?.id;

  event.notification.close();

  // Abrir la ventana del navegador
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(windowClients => {
      // Buscar si ya hay una ventana abierta
      for (let i = 0; i < windowClients.length; i++) {
        const client = windowClients[i];
        if (client.url === '/' && 'focus' in client) {
          return client.focus();
        }
      }
      // Si no hay ventana, crear una nueva
      if (clients.openWindow) {
        return clients.openWindow(`/?incidente=${incidenteId}`);
      }
    })
  );
});

console.log('✅ Firebase Messaging Service Worker cargado');
