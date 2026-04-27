import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { IncidentesService } from '../../core/services/incidentes';
import { UsuariosService } from '../../core/services/usuarios'; 
import { environment } from '../../../environments/environment';
import * as L from 'leaflet';

@Component({
  selector: 'app-auxilios',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auxilios.html',
  styleUrl: './auxilios.css'
})
export class AuxiliosComponent implements OnInit {
  private incidentesService = inject(IncidentesService);
  private usuariosService = inject(UsuariosService);
  private http = inject(HttpClient);

  tabActiva: 'pendientes' | 'mis-atenciones' = 'pendientes';
  incidentesPendientes: any[] = [];
  misAtenciones: any[] = [];
  tecnicosDisponibles: any[] = []; 
  cargando: boolean = false;
  incidenteSeleccionado: any = null;

  // Estados de Modales
  mostrarModalCobro: boolean = false;
  mostrarModalAsignar: boolean = false; 
  mostrarModalRechazo: boolean = false; 

  // Datos temporales para las acciones
  incidenteAccion: any = null; 
  montoCobro: number = 0;
  idTecnicoSeleccionado: number = 0;
  motivoRechazo: string = '';

  ngOnInit() { 
    this.cargarDatos();
    this.cargarTecnicos();
  }

  cargarDatos() {
    this.cargando = true;
    this.incidentesService.getPendientes().subscribe(data => this.incidentesPendientes = data);
    this.incidentesService.getMisAtenciones().subscribe(data => {
      this.misAtenciones = data;
      this.cargando = false;
    });
  }

  cargarTecnicos() {
    this.usuariosService.getMisTecnicos().subscribe(data => {
      // Filtramos solo los que el taller marcó como activos
      this.tecnicosDisponibles = data.filter((t: any) => t.esta_activo);
    });
  }

  cambiarTab(tab: 'pendientes' | 'mis-atenciones') { 
    this.tabActiva = tab; 
    this.incidenteSeleccionado = null; 
  }

  seleccionarIncidente(inc: any) { 
    this.incidenteSeleccionado = inc; 
    // Inicializar mapa después de que se renderice el template
    setTimeout(() => this.inicializarMapa(), 300);
  }

  private mapa: L.Map | null = null;

  inicializarMapa() {
    if (!this.incidenteSeleccionado) return;
    
    const lat = Number(this.incidenteSeleccionado.latitud);
    const lon = Number(this.incidenteSeleccionado.longitud);
    
    // Validar coordenadas
    if (!lat || !lon || lat < -90 || lat > 90 || lon < -180 || lon > 180) {
      console.error('Coordenadas inválidas:', lat, lon);
      return;
    }

    // Destruir mapa anterior si existe
    if (this.mapa) {
      this.mapa.remove();
      this.mapa = null;
    }

    // Crear nuevo mapa
    const mapContainer = document.getElementById('mapa-incidente');
    if (!mapContainer) return;

    this.mapa = L.map('mapa-incidente').setView([lat, lon], 15);

    // Agregar tile layer de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(this.mapa);

    // 📍 Marcador del incidente
    L.marker([lat, lon], {
      icon: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      })
    })
    .bindPopup(`<strong>Incidente #${this.incidenteSeleccionado.id}</strong><br>📍 ${lat.toFixed(4)}, ${lon.toFixed(4)}`)
    .addTo(this.mapa)
    .openPopup();
  }

  // --- LÓGICA DE ASIGNACIÓN Y REASIGNACIÓN ---

  // Se usa cuando aceptas un incidente nuevo
  aceptarIncidente(id: number) {
    this.incidentesService.aceptarIncidente(id).subscribe({
      next: (res) => {
        this.cargarDatos();
        this.incidenteAccion = res;
        this.idTecnicoSeleccionado = 0;
        this.mostrarModalAsignar = true;
      },
      error: (e) => alert('Error al aceptar: ' + e.error?.detail)
    });
  }

  // Se usa desde el panel lateral para cambiar al técnico
  abrirReasignacion() {
    if (!this.incidenteSeleccionado) return;
    this.incidenteAccion = this.incidenteSeleccionado;
    // Pre-seleccionamos el ID actual si ya tiene uno
    this.idTecnicoSeleccionado = this.incidenteSeleccionado.tecnico_id || 0;
    this.mostrarModalAsignar = true;
  }

  confirmarAsignacion() {
    if (!this.idTecnicoSeleccionado) return alert('Debes seleccionar un técnico.');
    
    this.incidentesService.asignarTecnico(this.incidenteAccion.id, this.idTecnicoSeleccionado).subscribe({
      next: () => {
        alert('Técnico asignado correctamente 🔧');
        
        // Actualización reactiva del panel lateral si está abierto
        const tecnicoNuevo = this.tecnicosDisponibles.find(t => t.id == this.idTecnicoSeleccionado);
        if (this.incidenteSeleccionado && this.incidenteSeleccionado.id === this.incidenteAccion.id) {
          this.incidenteSeleccionado.tecnico = tecnicoNuevo;
          this.incidenteSeleccionado.tecnico_id = this.idTecnicoSeleccionado;
        }

        this.cerrarModalAsignar();
        this.cargarDatos();
      },
      error: (e) => alert('Error en asignación: ' + e.error?.detail)
    });
  }

  cerrarModalAsignar() {
    this.mostrarModalAsignar = false;
    this.incidenteAccion = null;
    this.idTecnicoSeleccionado = 0;
  }

  // --- FLUJO DE RECHAZO ---

  abrirModalRechazo(inc: any) {
    this.incidenteAccion = inc;
    this.motivoRechazo = '';
    this.mostrarModalRechazo = true;
  }

  confirmarRechazo() {
    if (!this.motivoRechazo.trim()) return alert('Por favor escribe un motivo.');

    this.incidentesService.rechazarIncidente(this.incidenteAccion.id, this.motivoRechazo).subscribe({
      next: () => {
        alert('Pedido rechazado con éxito.');
        this.mostrarModalRechazo = false;
        if (this.incidenteSeleccionado?.id === this.incidenteAccion.id) {
          this.incidenteSeleccionado = null;
        }
        this.cargarDatos();
      },
      error: (e) => alert('Error al rechazar: ' + e.error?.detail)
    });
  }

  // --- FINALIZACIÓN Y COBRO ---

  finalizarAyuda(id: number) {
    if (!confirm('¿Marcar el servicio como completado?')) return;
    this.incidentesService.actualizarEstado(id, { estado: 'atendido' }).subscribe({
      next: () => {
        if (this.incidenteSeleccionado?.id === id) {
          this.incidenteSeleccionado.estado = 'atendido';
        }
        this.cargarDatos();
      }
    });
  }

  abrirModalCobro(incidente: any) {
    this.incidenteAccion = incidente;
    this.montoCobro = 0;
    this.mostrarModalCobro = true;
  }

  cerrarModalCobro() {
    this.mostrarModalCobro = false;
    this.incidenteAccion = null;
  }
  generarCobro() {
    if (this.montoCobro <= 0) return alert('Monto inválido.');
  
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const url = `${environment.apiUrl}/pagos/generar-cobro/${this.incidenteAccion.id}?monto=${this.montoCobro}&metodo=por_definir`;

    this.http.post(url, {}, { headers }).subscribe({
      next: (res: any) => {
        // ✅ ELIMINADO: window.open (Ya no abre links externos)
        alert('Cobro registrado y emitido con éxito 💵');
      
        this.cerrarModalCobro();
        this.cargarDatos(); // 🔄 Recargamos para que el estado 'pago_estado' cambie en la tabla
      },
      error: (e) => alert('Error al generar cobro: ' + e.error?.detail)
    });
  }
}