import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TalleresService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/v1/talleres';

  private getHeaders() {
    return new HttpHeaders().set('Authorization', `Bearer ${localStorage.getItem('token')}`);
  }

  // Obtiene los datos del taller del admin logueado
  getMiTaller(): Observable<any> {
    return this.http.get(`${this.apiUrl}/me`, { headers: this.getHeaders() });
  }

  // Actualiza los datos
  updateMiTaller(data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/me`, data, { headers: this.getHeaders() });
  }
}