import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
// 👇 1. Importamos el environment global
import { environment } from '../../../environments/environment';

// --- INTERFACES DIRECTAS ---
export interface LoginRequest {
  username: string; 
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegistroSaaS {
  nombre: string;
  correo: string;
  password: string;
  taller: {
    nombre: string;
    direccion: string;
    latitud?: number;
    longitud?: number;
    comision_porcentaje?: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  // 👇 2. Cambiamos la base al environment de producción
  private baseUrl = `${environment.apiUrl}/auth`; 

  public isAuthenticated = signal<boolean>(this.hasToken());

  /**
   * REGISTRO SAAS: Crea Taller y Usuario Administrador al mismo tiempo
   */
  registerTaller(data: RegistroSaaS): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/register-taller`, data).pipe(
      tap((response) => {
        localStorage.setItem('token', response.access_token);
        this.isAuthenticated.set(true);
      })
    );
  }

  /**
   * LOGIN: Ingreso para usuarios existentes
   */
  login(credentials: LoginRequest): Observable<LoginResponse> {
    const body = new URLSearchParams();
    body.set('username', credentials.username);
    body.set('password', credentials.password);
    body.set('client_id', 'web');

    return this.http.post<LoginResponse>(`${this.baseUrl}/login`, body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).pipe(
      tap((response) => {
        localStorage.setItem('token', response.access_token);
        this.isAuthenticated.set(true);
      })
    );
  }
  
  /**
   * LOGOUT: Limpia el token y el estado
   */
  logout(): void {
    localStorage.removeItem('token');
    localStorage.clear();
    this.isAuthenticated.set(false);
  }

  /**
   * VERIFICADOR: Revisa si hay una sesión activa al cargar la página
   */
  private hasToken(): boolean {
    if (typeof window !== 'undefined' && localStorage) {
      return !!localStorage.getItem('token');
    }
    return false;
  }

  // ==========================================
  // --- MÉTODOS DE RECUPERACIÓN DE CLAVE ---
  // ==========================================

  solicitarRecuperacion(correo: string) {
    // Apunta a /api/v1/auth/forgot-password
    return this.http.post(`${this.baseUrl}/forgot-password`, { correo });
  }

  restablecerClave(token: string, nueva_clave: string) {
    // Apunta a /api/v1/auth/reset-password
    return this.http.post(`${this.baseUrl}/reset-password`, { 
      token: token, 
      nueva_clave: nueva_clave 
    });
  }
}