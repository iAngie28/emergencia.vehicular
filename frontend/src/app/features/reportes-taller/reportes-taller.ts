import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReportesService, Reporte } from '../../core/services/reportes';

@Component({
  selector: 'app-reportes-taller',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reportes-taller.html',
  styleUrls: ['./reportes-taller.css']
})
export class ReportesTallerComponent implements OnInit {
  private reportesService = inject(ReportesService);

  reportes: Reporte[] = [];
  mostrarModalResolver = false;
  reporteSeleccionado: Reporte | null = null;
  respuestaTaller = '';
  cargando = false;

  ngOnInit() {
    this.cargarReportes();
  }

  cargarReportes() {
    this.reportesService.obtenerReportes().subscribe({
      next: (data) => {
        // En teoría, el backend ya filtra por taller y solo retorna los de tipo 'tecnico'
        this.reportes = data;
      },
      error: (err) => console.error('Error cargando reportes:', err)
    });
  }

  abrirModalResolver(reporte: Reporte) {
    this.reporteSeleccionado = reporte;
    this.respuestaTaller = reporte.respuesta || '';
    this.mostrarModalResolver = true;
  }

  cerrarModalResolver() {
    this.reporteSeleccionado = null;
    this.respuestaTaller = '';
    this.mostrarModalResolver = false;
  }

  guardarResolucion() {
    if (!this.reporteSeleccionado || !this.respuestaTaller.trim()) return;

    this.cargando = true;
    this.reportesService.responderReporte(this.reporteSeleccionado.id, this.respuestaTaller).subscribe({
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
