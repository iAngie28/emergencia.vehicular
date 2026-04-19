import { Injectable, inject } from '@angular/core'; // 👈 Esto viene de @angular/core
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class UsuariosService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/v1/usuarios';

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

  // src/app/core/services/usuarios.ts

  actualizarAdmin(id: number, datos: any) {
  // 🚩 USAR getHeaders() es vital para evitar el 401
    return this.http.put(`${this.apiUrl}/${id}`, datos, { 
      headers: this.getHeaders() 
    });
  }
}