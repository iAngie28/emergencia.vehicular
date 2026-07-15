import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReportesService, Reporte } from '../../core/services/reportes';
import { AuthService } from '../../core/services/auth';

@Component({
  selector: 'app-reportes-taller',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reportes-taller.html',
  styleUrls: ['./reportes-taller.css']
})
export class ReportesTallerComponent implements OnInit {
  private reportesService = inject(ReportesService);
  private authService = inject(AuthService);

  reportes: Reporte[] = [];
  mostrarModalResolver = false;
  reporteSeleccionado: Reporte | null = null;
  respuestaReporte = '';
  cargando = false;
  modoSuperadminGlobal = false;

  ngOnInit() {
    const rolOriginal = localStorage.getItem('original_rol_id') || localStorage.getItem('rol_id');
    this.modoSuperadminGlobal = rolOriginal === '4' && !this.authService.isImpersonating();
    this.cargarReportes();
  }

  get tituloPagina(): string {
    return this.modoSuperadminGlobal ? 'Reportes de Talleres' : 'Reportes sobre Técnicos';
  }

  get subtituloPagina(): string {
    return this.modoSuperadminGlobal
      ? 'Gestiona las quejas e incidencias registradas por los clientes contra los talleres afiliados.'
      : 'Gestiona las quejas e incidencias registradas por los clientes contra tus técnicos asignados.';
  }

  get iconoPagina(): string {
    return this.modoSuperadminGlobal ? 'fa-warehouse' : 'fa-user-ninja';
  }

  get reportadoHeader(): string {
    return this.modoSuperadminGlobal ? 'Taller Reportado' : 'Técnico Reportado';
  }

  get emptyMessage(): string {
    return this.modoSuperadminGlobal
      ? 'No se han registrado reportes contra talleres.'
      : 'No se han registrado reportes contra tus técnicos. ¡Buen trabajo!';
  }

  get respuestaLabel(): string {
    return this.modoSuperadminGlobal
      ? 'Respuesta Oficial de la Plataforma:'
      : 'Descargo / Respuesta del Taller:';
  }

  get respuestaPlaceholder(): string {
    return this.modoSuperadminGlobal
      ? 'Escribe la respuesta o solución que se le dará al cliente...'
      : 'Describe las acciones correctivas o explicaciones que se le darán al cliente...';
  }

  cargarReportes() {
    this.reportesService.obtenerReportes().subscribe({
      next: (data) => {
        this.reportes = data;
      },
      error: (err) => console.error('Error cargando reportes:', err)
    });
  }

  abrirModalResolver(reporte: Reporte) {
    this.reporteSeleccionado = reporte;
    this.respuestaReporte = reporte.respuesta || '';
    this.mostrarModalResolver = true;
  }

  cerrarModalResolver() {
    this.reporteSeleccionado = null;
    this.respuestaReporte = '';
    this.mostrarModalResolver = false;
  }

  guardarResolucion() {
    if (!this.reporteSeleccionado || !this.respuestaReporte.trim()) return;

    this.cargando = true;
    this.reportesService.responderReporte(this.reporteSeleccionado.id, this.respuestaReporte).subscribe({
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
