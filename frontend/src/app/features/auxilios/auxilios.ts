import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { IncidentesService } from '../../core/services/incidentes';
// 👇 1. Importamos el environment
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-auxilios',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auxilios.html',
  styleUrl: './auxilios.css'
})
export class AuxiliosComponent implements OnInit {
  private incidentesService = inject(IncidentesService);
  private http = inject(HttpClient);

  tabActiva: 'pendientes' | 'mis-atenciones' = 'pendientes';
  incidentesPendientes: any[] = [];
  misAtenciones: any[] = [];
  cargando: boolean = false;
  incidenteSeleccionado: any = null;

  mostrarModalCobro: boolean = false;
  incidenteACobrar: any = null;
  montoCobro: number = 0;

  ngOnInit() { this.cargarDatos(); }

  cambiarTab(tab: 'pendientes' | 'mis-atenciones') { 
    this.tabActiva = tab; 
    this.incidenteSeleccionado = null; 
  }

  cargarDatos() {
    this.cargando = true;
    this.incidentesService.getPendientes().subscribe({
      next: (data) => this.incidentesPendientes = data,
      error: () => this.cargando = false
    });

    this.incidentesService.getMisAtenciones().subscribe({
      next: (data) => {
        this.misAtenciones = data;
        this.cargando = false;
      },
      error: () => this.cargando = false
    });
  }

  verDetalle(incidente: any) { this.incidenteSeleccionado = incidente; }
  cerrarDetalle() { this.incidenteSeleccionado = null; }

  aceptarAuxilio(id: number) {
    if (!confirm('¿Atender este auxilio?')) return;
    this.incidentesService.aceptarIncidente(id).subscribe({
      next: () => {
        this.incidentesPendientes = this.incidentesPendientes.filter(i => i.id !== id);
        this.tabActiva = 'mis-atenciones';
        this.cargarDatos(); 
      }
    });
  }

  finalizarAuxilio(id: number) {
    if (!confirm('¿Marcar el servicio como completado?')) return;
    this.incidentesService.actualizarEstado(id, { estado: 'atendido' }).subscribe({
      next: () => {
        this.misAtenciones = this.misAtenciones.map(inc => 
          inc.id === id ? { ...inc, estado: 'atendido' } : inc
        );
        this.cargarDatos();
      }
    });
  }

  abrirModalCobro(incidente: any) {
    this.incidenteACobrar = incidente;
    this.montoCobro = 0;
    this.mostrarModalCobro = true;
  }

  cerrarModalCobro() {
    this.mostrarModalCobro = false;
    this.incidenteACobrar = null;
  }

  generarCobro() {
    if (this.montoCobro <= 0) return alert('Por favor ingresa un monto válido mayor a 0.');
    
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    // 👇 2. Usamos el link global para arreglar el CORS de los pagos
    const url = `${environment.apiUrl}/pagos/generar-cobro/${this.incidenteACobrar.id}?monto=${this.montoCobro}&metodo=por_definir`;

    this.http.post(url, {}, { headers }).subscribe({
      next: () => {
        alert('Cobro emitido y enviado a Finanzas 💸');
        this.misAtenciones = this.misAtenciones.map(inc => 
          inc.id === this.incidenteACobrar.id ? { ...inc, pago_estado: 'por_cobrar' } : inc
        );
        this.cerrarModalCobro();
      },
      error: (err) => alert('Error al generar cobro: ' + err.error?.detail)
    });
  }
}