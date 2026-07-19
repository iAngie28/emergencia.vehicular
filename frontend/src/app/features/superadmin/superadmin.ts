import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { environment } from '../../../environments/environment';
import { TalleresService } from '../../core/services/talleres';
import { ReportesService, Reporte } from '../../core/services/reportes';
import { AuthService } from '../../core/services/auth';
import { NotificacionContadorService } from '../../core/services/notificacion-contador.service';
import { WebSocketNotificacionService } from '../../core/services/websocket-notificacion.service';

interface SuperadminNotificacion {
  id: number;
  titulo: string;
  mensaje: string;
  tipo: string;
  leido: boolean;
  fecha_envio: string;
  incidente_id?: number;
}

@Component({
  selector: 'app-superadmin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './superadmin.html',
  styleUrls: ['./superadmin.css']
})
export class SuperadminComponent implements OnInit, OnDestroy {
  private http = inject(HttpClient);
  private talleresService = inject(TalleresService);
  private reportesService = inject(ReportesService);
  private authService = inject(AuthService);
  private contadorNotificaciones = inject(NotificacionContadorService);
  private wsService = inject(WebSocketNotificacionService);
  private router = inject(Router);
  private notificacionSub: Subscription | null = null;
  private contadorSub: Subscription | null = null;

  talleres: any[] = [];
  reportes: Reporte[] = [];
  notificaciones: SuperadminNotificacion[] = [];
  notificacionesNoLeidas = 0;
  cargandoNotificaciones = false;
  tabActiva: 'talleres' | 'reportes' | 'notificaciones' = 'talleres';
  filtrosTaller = {
    nombre: '',
    ciudad: '',
    estado: '',
    fecha_desde: '',
    fecha_hasta: ''
  };

  mostrarModalDetalle = false;
  detalleTaller: any = null;
  cargandoDetalle = false;
  mostrarModalInhabilitar = false;
  tallerParaInhabilitar: any = null;
  datosInhabilitacion = {
    tipo_inhabilitacion: 'temporal',
    motivo: ''
  };
  procesandoInhabilitacion = false;
  
  // Modal de resolución de reporte
  mostrarModalResolver = false;
  reporteSeleccionado: Reporte | null = null;
  respuestaAdmin = '';
  cargando = false;

  ngOnInit() {
    this.cargarTalleres();
    this.cargarReportes();
    this.inicializarNotificaciones();
  }

  ngOnDestroy() {
    this.notificacionSub?.unsubscribe();
    this.contadorSub?.unsubscribe();
  }

  private getHeaders() {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  cargarTalleres() {
    const filtros = {
      ...this.filtrosTaller,
      estado: this.filtrosTaller.estado === '' ? '' : this.filtrosTaller.estado === 'true'
    };

    this.talleresService.listarTodos(filtros).subscribe({
      next: (data) => {
        this.talleres = data;
      },
      error: (err) => console.error('Error cargando talleres:', err)
    });
  }

  aplicarFiltrosTaller() {
    this.cargarTalleres();
  }

  limpiarFiltrosTaller() {
    this.filtrosTaller = {
      nombre: '',
      ciudad: '',
      estado: '',
      fecha_desde: '',
      fecha_hasta: ''
    };
    this.cargarTalleres();
  }

  cargarReportes() {
    this.reportesService.obtenerReportes().subscribe({
      next: (data) => {
        this.reportes = data;
      },
      error: (err) => console.error('Error cargando reportes:', err)
    });
  }

  cambiarTab(tab: 'talleres' | 'reportes' | 'notificaciones') {
    this.tabActiva = tab;
    if (tab === 'notificaciones') {
      this.cargarNotificaciones();
    }
  }

  nombreTallerReportado(reporte?: Reporte | null): string {
    if (!reporte) return 'N/A';
    return reporte.taller_nombre || (reporte.taller_id ? `#${reporte.taller_id}` : 'N/A');
  }

  abrirDetalleTaller(taller: any) {
    this.mostrarModalDetalle = true;
    this.detalleTaller = null;
    this.cargandoDetalle = true;

    this.talleresService.obtenerDetalleSuperadmin(taller.id).subscribe({
      next: (data) => {
        this.detalleTaller = data;
        this.cargandoDetalle = false;
      },
      error: (err) => {
        this.cargandoDetalle = false;
        console.error('Error cargando detalle del taller:', err);
        alert('No se pudo cargar el detalle del taller.');
        this.cerrarDetalleTaller();
      }
    });
  }

  cerrarDetalleTaller() {
    this.mostrarModalDetalle = false;
    this.detalleTaller = null;
    this.cargandoDetalle = false;
  }

  abrirInhabilitarTaller(taller: any = this.detalleTaller?.taller) {
    if (!taller || !taller.estado) return;
    this.tallerParaInhabilitar = taller;
    this.datosInhabilitacion = {
      tipo_inhabilitacion: 'temporal',
      motivo: ''
    };
    this.mostrarModalInhabilitar = true;
  }

  cerrarInhabilitarTaller() {
    this.mostrarModalInhabilitar = false;
    this.tallerParaInhabilitar = null;
    this.procesandoInhabilitacion = false;
    this.datosInhabilitacion = {
      tipo_inhabilitacion: 'temporal',
      motivo: ''
    };
  }

  confirmarInhabilitarTaller() {
    if (!this.tallerParaInhabilitar || this.datosInhabilitacion.motivo.trim().length < 5) {
      alert('Debes registrar un motivo de al menos 5 caracteres.');
      return;
    }

    this.procesandoInhabilitacion = true;
    this.talleresService.inhabilitarTaller(this.tallerParaInhabilitar.id, {
      tipo_inhabilitacion: this.datosInhabilitacion.tipo_inhabilitacion,
      motivo: this.datosInhabilitacion.motivo.trim()
    }).subscribe({
      next: (tallerActualizado) => {
        this.procesandoInhabilitacion = false;
        this.cerrarInhabilitarTaller();
        this.cargarTalleres();
        if (this.detalleTaller?.taller?.id === tallerActualizado.id) {
          this.abrirDetalleTaller(tallerActualizado);
        }
      },
      error: (err) => {
        this.procesandoInhabilitacion = false;
        const detail = err?.error?.detail;
        const mensaje = typeof detail === 'string'
          ? detail
          : detail?.mensaje || 'No se pudo inhabilitar el taller.';
        alert(mensaje);
      }
    });
  }

  nombreTecnico(tecnico: any): string {
    return [tecnico?.nombre, tecnico?.apellido].filter(Boolean).join(' ') || 'Sin nombre';
  }

  formatearFecha(fecha?: string): string {
    if (!fecha) return 'Sin fecha';
    const date = new Date(fecha);
    if (Number.isNaN(date.getTime())) return 'Sin fecha';

    return date.toLocaleDateString('es-BO', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  }

  etiquetaEstadoTaller(estado: boolean): string {
    return estado ? 'Habilitado' : 'Inhabilitado';
  }

  etiquetaTipoInhabilitacion(tipo?: string): string {
    if (tipo === 'permanente') return 'Permanente';
    if (tipo === 'temporal') return 'Temporal';
    return 'No registrada';
  }

  inicializarNotificaciones() {
    const usuarioId = Number(localStorage.getItem('usuario_id'));
    if (Number.isFinite(usuarioId) && usuarioId > 0) {
      this.wsService.conectar(usuarioId);
    }

    this.contadorSub = this.contadorNotificaciones.noLeidas$.subscribe((cantidad) => {
      this.notificacionesNoLeidas = cantidad;
    });

    this.notificacionSub = this.wsService.notificaciones$.subscribe((notificacion) => {
      if (!notificacion) return;
      this.agregarNotificacionReciente(notificacion);
      this.contadorNotificaciones.cargarPendientes();
    });

    this.cargarNotificaciones();
    this.contadorNotificaciones.cargarPendientes();
  }

  cargarNotificaciones() {
    const usuarioId = localStorage.getItem('usuario_id');
    if (!usuarioId) {
      this.notificaciones = [];
      this.cargandoNotificaciones = false;
      return;
    }

    this.cargandoNotificaciones = true;
    this.http.get<SuperadminNotificacion[]>(
      `${environment.apiUrl}/notificaciones/usuario/${usuarioId}/historial`,
      { headers: this.getHeaders() }
    ).subscribe({
      next: (data) => {
        this.notificaciones = data;
        this.cargandoNotificaciones = false;
        this.contadorNotificaciones.cargarPendientes();
      },
      error: (err) => {
        this.cargandoNotificaciones = false;
        console.error('Error cargando notificaciones del superadmin:', err);
      }
    });
  }

  marcarNotificacionComoLeida(notificacion: SuperadminNotificacion) {
    if (notificacion.leido) return;

    this.notificaciones = this.notificaciones.map((item) =>
      item.id === notificacion.id ? { ...item, leido: true } : item
    );
    this.contadorNotificaciones.descontarUna();

    this.contadorNotificaciones.marcarLeida(notificacion.id).subscribe({
      next: () => this.contadorNotificaciones.cargarPendientes(),
      error: () => {
        this.cargarNotificaciones();
        this.contadorNotificaciones.cargarPendientes();
      }
    });
  }

  iconoNotificacion(tipo: string): string {
    if (tipo === 'reporte_registrado') return 'fa-triangle-exclamation';
    if (tipo === 'reporte_respondido') return 'fa-reply';
    if (tipo === 'taller_inhabilitado') return 'fa-ban';
    return 'fa-bell';
  }

  private agregarNotificacionReciente(notificacion: Partial<SuperadminNotificacion>) {
    if (!notificacion.id || this.notificaciones.some((item) => item.id === notificacion.id)) {
      return;
    }

    this.notificaciones = [{
      id: notificacion.id,
      titulo: notificacion.titulo || 'Nueva notificación',
      mensaje: notificacion.mensaje || '',
      tipo: notificacion.tipo || 'sistema',
      leido: false,
      fecha_envio: notificacion.fecha_envio || new Date().toISOString(),
      incidente_id: notificacion.incidente_id
    }, ...this.notificaciones];
  }

  impersonar(tallerId: number) {
    this.cargando = true;
    this.authService.impersonarTaller(tallerId).subscribe({
      next: () => {
        this.cargando = false;
        // Redirigir al dashboard del taller impersonado
        this.router.navigate(['/dashboard']).then(() => {
          window.location.reload();
        });
      },
      error: (err) => {
        this.cargando = false;
        console.error('Error de impersonación:', err);
        alert('No se pudo impersonar el taller. Intente nuevamente.');
      }
    });
  }

  abrirModalResolver(reporte: Reporte) {
    this.reporteSeleccionado = reporte;
    this.respuestaAdmin = reporte.respuesta || '';
    this.mostrarModalResolver = true;
  }

  cerrarModalResolver() {
    this.reporteSeleccionado = null;
    this.respuestaAdmin = '';
    this.mostrarModalResolver = false;
  }

  guardarResolucion() {
    if (!this.reporteSeleccionado || !this.respuestaAdmin.trim()) return;

    this.cargando = true;
    this.reportesService.responderReporte(this.reporteSeleccionado.id, this.respuestaAdmin).subscribe({
      next: () => {
        this.cargando = false;
        this.cargarReportes();
        this.cerrarModalResolver();
      },
      error: (err) => {
        this.cargando = false;
        console.error('Error resolviendo reporte:', err);
        alert('Ocurrió un error al enviar la respuesta.');
      }
    });
  }
}
