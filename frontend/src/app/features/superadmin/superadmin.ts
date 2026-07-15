import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TalleresService } from '../../core/services/talleres';
import { ReportesService, Reporte } from '../../core/services/reportes';
import { AuthService } from '../../core/services/auth';

@Component({
  selector: 'app-superadmin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './superadmin.html',
  styleUrls: ['./superadmin.css']
})
export class SuperadminComponent implements OnInit {
  private talleresService = inject(TalleresService);
  private reportesService = inject(ReportesService);
  private authService = inject(AuthService);
  private router = inject(Router);

  talleres: any[] = [];
  reportes: Reporte[] = [];
  tabActiva: 'talleres' | 'reportes' = 'talleres';
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

  cambiarTab(tab: 'talleres' | 'reportes') {
    this.tabActiva = tab;
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
