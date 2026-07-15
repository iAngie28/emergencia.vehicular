import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.getRegistrations().then((registrations) => {
      registrations
        .filter((registration) => registration.active?.scriptURL.includes('ngsw-worker.js'))
        .forEach((registration) => registration.unregister());
    });

    if ('caches' in window) {
      caches.keys().then((keys) => {
        keys
          .filter((key) => key.startsWith('ngsw:') || key.includes('ngsw'))
          .forEach((key) => caches.delete(key));
      });
    }
  });
}

bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));
