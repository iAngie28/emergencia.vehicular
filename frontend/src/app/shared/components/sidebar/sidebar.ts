import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css'
})
export class SidebarComponent implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);

  // 🚩 Variable que alimenta el HTML
  public usuario: string = 'Cargando...';

  ngOnInit() {
    this.cargarDatosUsuario();
  }

  cargarDatosUsuario() {
    const token = localStorage.getItem('token');
    
    // Si no hay token, no intentamos pedir el perfil
    if (!token) return;

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    // Usamos el mismo endpoint que tu dashboard
    this.http.get<any>('http://localhost:8000/api/v1/usuarios/me', { headers }).subscribe({
      next: (user) => {
        // Asignamos el nombre real (ej: "Angie")
        this.usuario = user.nombre;
      },
      error: () => {
        this.usuario = 'Administrador';
      }
    });
  }

  onLogout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
}