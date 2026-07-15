import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
}

@Injectable({
  providedIn: 'root'
})
export class ReportesService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/reportes`;

  obtenerReportes(): Observable<Reporte[]> {
    return this.http.get<Reporte[]>(`${this.baseUrl}/`);
  }

  responderReporte(id: number, respuesta: string, estado: string = 'resuelto'): Observable<Reporte> {
    return this.http.patch<Reporte>(`${this.baseUrl}/${id}/responder`, {
      respuesta,
      estado
    });
  }

  crearReporte(reporte: any): Observable<Reporte> {
    return this.http.post<Reporte>(`${this.baseUrl}/`, reporte);
  }
}
