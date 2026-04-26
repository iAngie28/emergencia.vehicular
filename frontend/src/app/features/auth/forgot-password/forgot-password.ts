import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../core/services/auth';
import { Router } from '@angular/router';
@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './forgot-password.html',
  styleUrls: ['./forgot-password.css'] 
})
export class ForgotPasswordComponent {
  correo: string = '';
  mensaje: string = '';
  error: string = '';
  cargando: boolean = false; // 👈 Antes era 'loading'

  private authService = inject(AuthService);
  private router = inject(Router);

  // 👈 Tu HTML llama a 'enviar()'
  enviar() {
    this.cargando = true;
    this.error = '';
    
    this.authService.solicitarRecuperacion(this.correo).subscribe({
      next: (res: any) => {
        this.mensaje = 'Si el correo existe, recibirás un enlace en breve.';
        this.cargando = false;
      },
      error: (e: any) => {
        this.error = 'Ocurrió un error al procesar la solicitud.';
        this.cargando = false;
      }
    });
  }
}