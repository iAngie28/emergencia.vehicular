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
    this.talleresService.listarTodos().subscribe({
      next: (data) => {
        this.talleres = data;
      },
      error: (err) => console.error('Error cargando talleres:', err)
    });
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
