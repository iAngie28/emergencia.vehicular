import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth';
import { WebSocketNotificacionService } from '../../core/services/websocket-notificacion.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-taller-inhabilitado',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './taller-inhabilitado.html',
  styleUrls: ['./taller-inhabilitado.css']
})
export class TallerInhabilitadoComponent implements OnInit, OnDestroy {
  private subs = new Subscription();

  constructor(
    private authService: AuthService, 
    private router: Router,
    private wsService: WebSocketNotificacionService
  ) {}

  ngOnInit() {
    const usuarioId = Number(localStorage.getItem('usuario_id'));
    if (Number.isFinite(usuarioId) && usuarioId > 0) {
      this.wsService.conectar(usuarioId);
      
      this.subs.add(
        this.wsService.notificaciones$.subscribe((notificacion) => {
          if (notificacion && notificacion.tipo === 'taller_habilitado') {
            localStorage.setItem('auth_taller_estado', 'true');
            this.router.navigate(['/']);
          }
        })
      );
    }
  }

  ngOnDestroy() {
    this.subs.unsubscribe();
    this.wsService.desconectar();
  }

  cerrarSesion() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
