import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class IncidentesService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/incidentes`; 

  private getHeaders() {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  // 1. Obtener incidentes pendientes
  getPendientes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pendientes`, { headers: this.getHeaders() });
  }

  // 2. Obtener incidentes de mi taller
  getMisAtenciones(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/mis-atenciones`, { headers: this.getHeaders() });
  }

  // 3. Aceptar un incidente
  aceptarIncidente(id: number): Observable<any> {
    return this.http.patch(`${this.apiUrl}/${id}/aceptar`, {}, { headers: this.getHeaders() });
  }

  // 🚀 NUEVO: Asignar un técnico específico
  asignarTecnico(incidenteId: number, tecnicoId: number): Observable<any> {
    const params = new HttpParams().set('tecnico_id', tecnicoId.toString());
    return this.http.patch(`${this.apiUrl}/${incidenteId}/asignar-tecnico`, {}, { 
      headers: this.getHeaders(),
      params: params
    });
  }

  // 🚀 NUEVO: Rechazar pedido con motivo
  rechazarIncidente(id: number, motivo: string): Observable<any> {
    const params = new HttpParams().set('motivo', motivo);
    return this.http.patch(`${this.apiUrl}/${id}/rechazar`, {}, { 
      headers: this.getHeaders(),
      params: params
    });
  }

  // 4. Actualizar estado (Finalizar)
  actualizarEstado(id: number, datos: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, datos, { headers: this.getHeaders() });
  }
}