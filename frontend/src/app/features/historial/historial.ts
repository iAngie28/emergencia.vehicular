import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IncidentesService } from '../../core/services/incidentes';
import { Incidente } from '../../interface/incidente.interface';

@Component({
  selector: 'app-historial',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './historial.html',  // 👈 Corregido el nombre del archivo
  styleUrl: './historial.css'       // 👈 Corregido el nombre del archivo
})
export class HistorialComponent implements OnInit {
  // 👈 Corregido el nombre a IncidentesService
  private incidentesService = inject(IncidentesService);

  historial: Incidente[] = [];
  metricas: any = null;
  cargando = false;

  // Filtros de fecha
  fechaInicio: string = '';
  fechaFin: string = '';

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargando = true;
    
    // 1. Cargar las tarjetas de métricas
    this.incidentesService.obtenerMetricas().subscribe({
      next: (data: any) => this.metricas = data, // 👈 Se agregó ": any"
      error: (err: any) => console.error('Error cargando métricas:', err) // 👈 Se agregó ": any"
    });

    // 2. Cargar la tabla del historial
    this.incidentesService.obtenerHistorial(this.fechaInicio, this.fechaFin).subscribe({
      next: (data: Incidente[]) => { // 👈 Se agregó el tipo
        this.historial = data;
        this.cargando = false;
      },
      error: (err: any) => { // 👈 Se agregó ": any"
        console.error('Error cargando historial:', err);
        this.cargando = false;
      }
    });
  }

  aplicarFiltros() {
    this.cargarDatos();
  }
}