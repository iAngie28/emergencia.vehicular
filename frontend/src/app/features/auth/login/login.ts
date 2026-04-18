import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService, LoginRequest } from '../../../core/services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.html', 
  styleUrls: ['./login.css'] 
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  loginForm = this.fb.group({
    username: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(3)]]
  });

  errorMessage = '';
  isLoading = false;

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';

    const credentials: LoginRequest = {
      username: this.loginForm.value.username!,
      password: this.loginForm.value.password!
    };

    this.authService.login(credentials).subscribe({
      next: (res: any) => { // Usamos 'any' por si tu interfaz no tiene access_token definido
        this.isLoading = false;
        console.log('Login exitoso, guardando token y redirigiendo...');
        localStorage.setItem('token', res.access_token); 
        
        this.router.navigate(['/dashboard']); 
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'Credenciales incorrectas o error de servidor.';
        console.error(err);
      }
    });
  }
}