import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BitacoraEntry {
  id: number;
  tabla: string;
  accion: string;
  valor_anterior: any;
  valor_nuevo: any;
  fecha_hora: string;
  usuario_id: number;
  taller_id: number;
  usuario_nombre?: string;
  tabla_id?: number;
}

@Injectable({ providedIn: 'root' })
export class BitacoraService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/v1/bitacora/';

  getLogs(skip: number = 0, limit: number = 100): Observable<BitacoraEntry[]> {
    const token = localStorage.getItem('token'); 
    
    // 1. Preparamos el Header
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    // 2. Preparamos los parámetros de la URL
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    // 3. ENVIAMOS AMBOS (Headers y Params)
    // Fíjate cómo van dentro del mismo bloque de llaves {}
    return this.http.get<BitacoraEntry[]>(this.apiUrl, { headers, params });
  }
}