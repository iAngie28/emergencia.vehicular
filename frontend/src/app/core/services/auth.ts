import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface LoginRequest {
  username: string; 
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/v1/auth/login'; 

  public isAuthenticated = signal<boolean>(this.hasToken());

  login(credentials: LoginRequest): Observable<LoginResponse> {
    // Formato URLSearchParams para OAuth2PasswordRequestForm de FastAPI
    const body = new URLSearchParams();
    body.set('username', credentials.username);
    body.set('password', credentials.password);

    return this.http.post<LoginResponse>(this.apiUrl, body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).pipe(
      tap((response) => {
        localStorage.setItem('access_token', response.access_token);
        this.isAuthenticated.set(true);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    this.isAuthenticated.set(false);
  }

  private hasToken(): boolean {
    if (typeof window !== 'undefined' && localStorage) {
      return !!localStorage.getItem('access_token');
    }
    return false;
  }
}