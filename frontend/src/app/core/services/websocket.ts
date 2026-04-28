import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class WebSocketService {
  private notificaciones$ = new BehaviorSubject<any>(null);
  
  get notificaciones(): Observable<any> {
    return this.notificaciones$.asObservable();
  }

  // Este servicio será reemplazado por Firebase
  conectar() {
    console.log('⏳ Notificaciones ahora se manejan con Firebase');
  }

  desconectar() {
    console.log('🛑 Firebase desactivado');
  }
}
