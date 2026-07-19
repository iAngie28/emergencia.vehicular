import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router } from '@angular/router';
import { SidebarComponent } from '../../components/sidebar/sidebar';
import { WebSocketNotificacionService } from '../../../core/services/websocket-notificacion.service';
import { AuthService } from '../../../core/services/auth';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, SidebarComponent],
  template: `
    <div class="layout-container">
      <app-sidebar></app-sidebar> 

      <main class="main-content">
        <!-- Banner de Impersonación -->
        <div class="impersonate-banner" *ngIf="authService.isImpersonating()">
          <div class="banner-text">
            <i class="fa-solid fa-triangle-exclamation pulse-warn"></i>
            <span>Sesión activa de Impersonación. Actuando como administrador de taller.</span>
          </div>
          <button class="btn-revert" (click)="revertir()" [disabled]="cargando">
            <i class="fa-solid fa-arrow-right-to-bracket"></i> Volver a Superadmin
          </button>
        </div>

        <div class="content-wrapper">
          <router-outlet></router-outlet>
        </div>
      </main>
    </div>
  `,
  styles: [`
    .layout-container {
      display: flex;
      min-height: 100vh;
      background-color: #f1f5f9; /* Color Slate 100 - Muy limpio */
    }

    .main-content {
      flex: 1;
      /* 🚩 EL TRUCO: Margen izquierdo igual al ancho del sidebar */
      margin-left: 260px; 
      height: 100vh;
      overflow-y: auto; /* Solo el contenido hace scroll, el sidebar queda fijo */
      display: flex;
      flex-direction: column;
    }

    .impersonate-banner {
      background: linear-gradient(90deg, #f59e0b, #d97706);
      color: #0f172a;
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      box-shadow: 0 4px 15px rgba(245, 158, 11, 0.25);
      z-index: 10;
      position: sticky;
      top: 0;
    }

    .impersonate-banner i {
      margin-right: 8px;
    }

    .pulse-warn {
      animation: pulse-warn 2s infinite;
    }
    @keyframes pulse-warn {
      0% { opacity: 1; }
      50% { opacity: 0.6; }
      100% { opacity: 1; }
    }

    .btn-revert {
      background: #0f172a;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
    }
    .btn-revert:hover:not(:disabled) {
      background: #1e293b;
      transform: scale(1.02);
    }
    .btn-revert:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }

    .content-wrapper {
      padding: 32px;
      flex: 1;
    }

    /* Ajuste para tablets/celulares */
    @media (max-width: 768px) {
      .main-content {
        margin-left: 0;
        height: auto;
        overflow-y: visible;
      }
      .content-wrapper {
        padding: 80px 16px 24px;
      }
    }
  `]
})
export class MainLayoutComponent implements OnInit, OnDestroy {
  private wsService = inject(WebSocketNotificacionService);
  public authService = inject(AuthService);
  private router = inject(Router);
  private subs = new Subscription();
  
  cargando = false;

  ngOnInit() {
    const usuarioId = Number(localStorage.getItem('usuario_id'));
    if (Number.isFinite(usuarioId) && usuarioId > 0) {
      this.wsService.conectar(usuarioId);
      
      this.subs.add(
        this.wsService.notificaciones$.subscribe((notificacion) => {
          if (notificacion && notificacion.tipo === 'taller_inhabilitado') {
            localStorage.setItem('auth_taller_estado', 'false');
            this.router.navigate(['/taller-inhabilitado']);
          }
        })
      );
    }
  }

  ngOnDestroy() {
    this.subs.unsubscribe();
    this.wsService.desconectar();
  }

  revertir() {
    this.cargando = true;
    this.authService.revertirImpersonacion().subscribe({
      next: () => {
        this.cargando = false;
        this.router.navigate(['/superadmin']).then(() => {
          window.location.reload();
        });
      },
      error: (err) => {
        this.cargando = false;
        console.error('Error al revertir:', err);
        alert('Ocurrió un error al revertir la impersonación.');
      }
    });
  }
}
