import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class IncidentesService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/v1/incidentes'; // Ajusta si tu puerto es distinto

  // Helper para los headers con el token de Rossy
  private getHeaders() {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  // 1. Obtener incidentes que nadie ha tomado (Pendientes)
  getPendientes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pendientes`, { headers: this.getHeaders() });
  }

  // 2. Obtener incidentes asignados a MI taller
  getMisAtenciones(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/mis-atenciones`, { headers: this.getHeaders() });
  }

  // 3. Aceptar un incidente (El taller toma el auxilio)
  aceptarIncidente(id: number): Observable<any> {
    // Mandamos un body vacío {} porque el taller_id lo saca el backend del token
    return this.http.patch(`${this.apiUrl}/${id}/aceptar`, {}, { headers: this.getHeaders() });
  }

  // 4. Finalizar o actualizar estado
  actualizarEstado(id: number, datos: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, datos, { headers: this.getHeaders() });
  }
}