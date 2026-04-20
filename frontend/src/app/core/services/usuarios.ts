import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
// 👇 1. Importa el environment (revisa que la ruta de carpetas sea la correcta según tu proyecto)
import { environment } from '../../../environments/environment'; 

@Injectable({ providedIn: 'root' })
export class UsuariosService {
  private http = inject(HttpClient);
  
  // 👇 2. Usa la variable global. Ya no escribas "localhost" ni el link de Render aquí.
  private apiUrl = `${environment.apiUrl}/usuarios`;

  private getHeaders() {
    return new HttpHeaders().set('Authorization', `Bearer ${localStorage.getItem('token')}`);
  }

  getMisAdmins(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/mis-administradores`, { headers: this.getHeaders() });
  }

  crearColega(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/nuevo-colega`, data, { headers: this.getHeaders() });
  }

  eliminarAdmin(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  actualizarAdmin(id: number, datos: any) {
    return this.http.put(`${this.apiUrl}/${id}`, datos, { 
      headers: this.getHeaders() 
    });
  }
}