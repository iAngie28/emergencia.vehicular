import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment'; 

@Injectable({ providedIn: 'root' })
export class UsuariosService {
  private http = inject(HttpClient);
  
  private apiUrl = `${environment.apiUrl}/usuarios`;
  private configUrl = `${environment.apiUrl}/taller-config`; // 👈 Prefijo para el catálogo

  private getHeaders() {
    return new HttpHeaders().set('Authorization', `Bearer ${localStorage.getItem('token')}`);
  }

  // --- ADMINISTRADORES ---
  getMisAdmins(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/mis-administradores`, { headers: this.getHeaders() });
  }

  crearColega(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/nuevo-colega`, data, { headers: this.getHeaders() });
  }

  actualizarAdmin(id: number, datos: any) {
    return this.http.put(`${this.apiUrl}/${id}`, datos, { headers: this.getHeaders() });
  }

  eliminarAdmin(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  // --- TÉCNICOS ---
  getMisTecnicos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/mis-tecnicos`, { headers: this.getHeaders() });
  }

  crearTecnico(data: any) {
    return this.http.post<any>(`${this.apiUrl}/nuevo-tecnico`, data, { headers: this.getHeaders() });
  }

  actualizarTecnico(id: number, data: any) {
    return this.http.put<any>(`${this.apiUrl}/tecnico/${id}`, data, { headers: this.getHeaders() });
  }

  // --- ESPECIALIDADES (Catálogo) ---
  getEspecialidades(): Observable<any[]> {
    return this.http.get<any[]>(`${this.configUrl}/especialidades`, { headers: this.getHeaders() });
  }

  // 🚀 ESTOS SON LOS QUE FALTABAN:
  crearEspecialidad(data: { nombre: string, descripcion: string }): Observable<any> {
    return this.http.post(`${this.configUrl}/especialidades`, data, { headers: this.getHeaders() });
  }

  eliminarEspecialidad(id: number): Observable<any> {
    return this.http.delete(`${this.configUrl}/especialidades/${id}`, { headers: this.getHeaders() });
  }
}