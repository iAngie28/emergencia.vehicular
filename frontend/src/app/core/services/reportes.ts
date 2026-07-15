import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Reporte {
  id: number;
  incidente_id: number;
  tipo_reporte: 'taller' | 'tecnico';
  motivo: string;
  descripcion: string;
  estado: 'abierto' | 'en_revision' | 'resuelto';
  respuesta?: string;
  fecha_creacion: string;
  fecha_resolucion?: string;
  usuario_id: number;
  taller_id: number;
  tecnico_id?: number;
  taller_nombre?: string;
  tecnico_nombre?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReportesService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/reportes`;

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  obtenerReportes(): Observable<Reporte[]> {
    return this.http.get<Reporte[]>(`${this.baseUrl}/`, { headers: this.getHeaders() });
  }

  responderReporte(id: number, respuesta: string, estado: string = 'resuelto'): Observable<Reporte> {
    return this.http.patch<Reporte>(`${this.baseUrl}/${id}/responder`, {
      respuesta,
      estado
    }, { headers: this.getHeaders() });
  }

  crearReporte(reporte: any): Observable<Reporte> {
    return this.http.post<Reporte>(`${this.baseUrl}/`, reporte, { headers: this.getHeaders() });
  }
}
