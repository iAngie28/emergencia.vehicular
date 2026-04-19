import { Component, inject, OnInit, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TalleresService } from '../../core/services/talleres';
import * as L from 'leaflet';

@Component({
  selector: 'app-perfil-taller',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './perfil-taller.html',
  styleUrl: './perfil-taller.css'
})
export class PerfilTallerComponent implements OnInit {
  private talleresService = inject(TalleresService);
  private zone = inject(NgZone); // 👈 Inyectamos NgZone
  private map: any;
  private marker: any;

  taller: any = {
    nombre: '',
    direccion: '',
    latitud: -17.7833,
    longitud: -63.1821,
    estado: true
  };

  cargando: boolean = false;
  mensaje: string = '';

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.talleresService.getMiTaller().subscribe({
      next: (data) => {
        this.taller = data;
        this.initMap();
      },
      error: (err) => {
        console.error('Error al cargar taller', err);
        this.initMap();
      }
    });
  }

  private initMap() {
    if (this.map) { this.map.remove(); }

    this.map = L.map('map').setView([this.taller.latitud, this.taller.longitud], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(this.map);

    const customIcon = L.icon({
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41]
    });

    this.marker = L.marker([this.taller.latitud, this.taller.longitud], { 
      icon: customIcon,
      draggable: true 
    }).addTo(this.map);

    // ✅ Al hacer clic en el mapa
    this.map.on('click', (e: any) => {
      this.actualizarCoordenadas(e.latlng.lat, e.latlng.lng);
    });

    // ✅ Al arrastrar el marcador
    this.marker.on('dragend', () => {
      const position = this.marker.getLatLng();
      this.actualizarCoordenadas(position.lat, position.lng);
    });
  }

  private actualizarCoordenadas(lat: number, lng: number) {
    // 🌀 Forzamos a Angular a actualizar la UI
    this.zone.run(() => {
      this.taller.latitud = lat;
      this.taller.longitud = lng;
    });
    this.marker.setLatLng([lat, lng]);
  }

  guardar() {
    this.cargando = true;
    this.mensaje = '';
    this.talleresService.updateMiTaller(this.taller).subscribe({
      next: () => {
        this.mensaje = '¡Perfil actualizado correctamente!';
        this.cargando = false;
        setTimeout(() => this.mensaje = '', 3000);
      },
      error: (err) => {
        console.error('Error al guardar', err);
        this.mensaje = 'Error al actualizar los datos.';
        this.cargando = false;
      }
    });
  }
}