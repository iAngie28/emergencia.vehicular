import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../core/services/auth';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule, RouterLinkActive],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.css']
})
export class SidebarComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  usuario: string = "Administrador"; // Esto lo podrías traer de un servicio de perfil

  onLogout() {
    this.authService.logout();
    this.router.navigate(['/']);
  }
}