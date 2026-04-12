import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../shared/components/sidebar/sidebar';


@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule], // <--- Deja solo el CommonModule
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  nombreTaller: string = "Taller Central Santa Cruz"; // Esto luego vendrá del API
  usuario: string = "Administrador";
  
  // Datos genéricos para mostrar algo en la web
  resumen = {
    incidentesHoy: 5,
    vehiculosEnReparacion: 3,
    completados: 12
  };

  incidentesRecientes = [
    { id: 1, vehiculo: 'Toyota Hilux - 123-ABC', estado: 'En Diagnóstico', prioridad: 'Alta' },
    { id: 2, vehiculo: 'Suzuki Vitara - 456-DEF', estado: 'Esperando Repuestos', prioridad: 'Media' },
    { id: 3, vehiculo: 'Nissan Frontier - 789-GHI', estado: 'Reparado', prioridad: 'Baja' }
  ];

  constructor() {}

  ngOnInit(): void {
    // Aquí podrías llamar a un servicio para traer los datos reales del taller
  }
}