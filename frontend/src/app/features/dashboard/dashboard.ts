import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html'
})
export class DashboardComponent implements OnInit {
  private http = inject(HttpClient);
  public tallerNombre: string = 'Cargando...';
  public usuarioNombre: string = 'Usuario';

  ngOnInit() {
    this.obtenerDatosPerfil();
  }

  obtenerDatosPerfil() {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    // Llamamos al endpoint que devuelve el usuario logueado
    this.http.get<any>('http://localhost:8000/api/v1/usuarios/me', { headers }).subscribe({
      next: (user) => {
        this.usuarioNombre = user.nombre;
        // Si tu backend devuelve el objeto taller dentro del usuario:
        if (user.taller) {
          this.tallerNombre = user.taller.nombre;
        } else {
          this.tallerNombre = "Mi Taller Pro";
        }
      },
      error: () => {
        this.tallerNombre = "Taller Pro";
      }
    });
  }
}