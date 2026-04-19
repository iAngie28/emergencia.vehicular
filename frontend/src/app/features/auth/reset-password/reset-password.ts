import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reset-password.html'
})
export class ResetPasswordComponent implements OnInit {
  token: string = '';
  nuevaClave: string = '';
  confirmarClave: string = ''; // 👈 Añadido porque tu HTML lo pide
  mensaje: string = '';
  error: string = '';
  cargando: boolean = false; // 👈 Cambiado de 'loading' a 'cargando'

  private route = inject(ActivatedRoute);
  private authService = inject(AuthService);
  private router = inject(Router);

  ngOnInit() {
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
    if (!this.token) {
      this.error = 'El token de recuperación no es válido o falta.';
    }
  }

  // 👈 Tu HTML llama a 'guardar()'
  guardar() {
    if (this.nuevaClave !== this.confirmarClave) {
      this.error = 'Las contraseñas no coinciden.';
      return;
    }

    this.cargando = true;
    this.authService.restablecerClave(this.token, this.nuevaClave).subscribe({
      next: (res: any) => {
        this.mensaje = 'Contraseña actualizada con éxito. Redirigiendo...';
        setTimeout(() => this.router.navigate(['/login']), 3000);
      },
      error: (e: any) => {
        this.error = 'El enlace ha expirado o ya fue utilizado.';
        this.cargando = false;
      }
    });
  }
}