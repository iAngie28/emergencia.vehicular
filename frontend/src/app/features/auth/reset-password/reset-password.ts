import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './reset-password.html',
  styleUrls: ['./reset-password.css']
})
export class ResetPasswordComponent implements OnInit {
  // Variables enlazadas al HTML
  nuevaClave: string = '';
  confirmarClave: string = '';
  mensaje: string = '';
  error: string = '';
  cargando: boolean = false;
  token: string = '';

  private authService = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  ngOnInit() {
    // Capturamos el token de la URL (?token=...)
    this.route.queryParams.subscribe(params => {
      this.token = params['token'] || '';
      if (!this.token) {
        this.error = 'Enlace inválido o expirado. Por favor solicita uno nuevo.';
      }
    });
  }

  cambiarPassword() {
    // Validaciones básicas antes de enviar
    if (this.nuevaClave !== this.confirmarClave) {
      this.error = 'Las contraseñas no coinciden.';
      return;
    }
    
    if (!this.token) {
      this.error = 'Token de seguridad no encontrado.';
      return;
    }

    this.cargando = true;
    this.error = '';
    this.mensaje = '';

    // Usamos el método correcto de tu AuthService: restablecerClave
    this.authService.restablecerClave(this.token, this.nuevaClave).subscribe({
      next: (res: any) => {
        this.mensaje = '¡Contraseña actualizada! Redirigiendo...';
        this.cargando = false;
        // Redirigir al login después de 2 segundos
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: (err: any) => {
        this.cargando = false;
        this.error = 'Error: El enlace ha expirado o ya fue utilizado.';
        console.error(err);
      }
    });
  }
}