import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './landing.html',
  styleUrls: ['./landing.css']
})
export class LandingComponent implements OnInit {
  private router = inject(Router);

  ngOnInit() {
    const token = localStorage.getItem('token');
    const rolId = Number(localStorage.getItem('rol_id') || 0);

    if (!token) return;

    if (rolId === 4) {
      this.router.navigateByUrl('/superadmin', { replaceUrl: true });
    } else if (rolId === 3) {
      this.router.navigateByUrl('/tecnico/dashboard', { replaceUrl: true });
    } else if (rolId === 1) {
      this.router.navigateByUrl('/dashboard', { replaceUrl: true });
    }
  }

  irALogin() {
    this.router.navigate(['/login']);
  }

  irARegistro() {
    this.router.navigate(['/registro-taller']);
  }

  irAPlanPremium() {
    const token = localStorage.getItem('token');
    if (token) {
      this.router.navigate(['/perfil-taller'], { queryParams: { checkout: 'true' } });
    } else {
      this.router.navigate(['/registro-taller'], { queryParams: { checkout: 'true' } });
    }
  }
}
