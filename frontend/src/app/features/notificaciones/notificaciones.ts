import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';

export interface Notificacion {
  id: number;
  titulo: string;
  mensaje: string;
  tipo: string;
  leido: boolean;
  fecha_envio: string;
  incidente_id?: number;
}

@Component({
  selector: 'app-notificaciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './notificaciones.html',
  styleUrl: './notificaciones.css'
})
export class NotificacionesComponent implements OnInit {
  private http = inject(HttpClient);
  
  public notificaciones: Notificacion[] = [];
  public cargando = true;

  private getHeaders() {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  ngOnInit() {
    this.cargarHistorial();
  }

  cargarHistorial() {
    const userId = localStorage.getItem('userId');
    if (!userId) return;

    // Llamamos al nuevo endpoint que trae TODAS (leídas y no leídas)
    this.http.get<Notificacion[]>(`${environment.apiUrl}/notificaciones/usuario/${userId}/historial`, { headers: this.getHeaders() })
      .subscribe({
        next: (data) => {
          this.notificaciones = data;
          this.cargando = false;
        },
        error: (err) => {
          console.error("Error cargando notificaciones", err);
          this.cargando = false;
        }
      });
  }

  marcarComoLeida(id: number) {
    // 🚩 OPTIMISTIC UI: Actualizamos visualmente primero
    this.notificaciones = this.notificaciones.map(noti => 
      noti.id === id ? { ...noti, leido: true } : noti
    );

    // Confirmamos con el Backend
    this.http.patch(`${environment.apiUrl}/notificaciones/${id}/leer`, {}, { headers: this.getHeaders() })
      .subscribe({
        error: () => this.cargarHistorial() // Si falla, recargamos los datos reales
      });
  }
}