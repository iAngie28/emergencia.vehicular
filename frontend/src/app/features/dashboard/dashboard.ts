import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html'
})
export class DashboardComponent implements OnInit {
  private http = inject(HttpClient);
  public tallerNombre: string = 'Cargando...';
  public usuarioNombre: string = 'Usuario';
  
  // KPIs Financieros
  public estadisticasFinanzas: any = {
    totalBruto: 0,
    totalComision: 0,
    totalNeto: 0,
    cantidadPagos: 0,
    cargando: true
  };

  ngOnInit() {
    this.obtenerDatosPerfil();
    this.cargarEstadisticasFinanzas();
  }

  obtenerDatosPerfil() {
    const token = localStorage.getItem('token');
    if (!token) return;
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    this.http.get<any>(`${environment.apiUrl}/usuarios/me`, { headers }).subscribe({
      next: (user) => {
        this.usuarioNombre = user.nombre;
        if (user.taller) {
          this.tallerNombre = user.taller.nombre;
        } else {
          this.tallerNombre = "Mi Taller Pro";
        }
      },
      error: () => {
        this.tallerNombre = "Taller Pro";
      }
    });
  }

  cargarEstadisticasFinanzas() {
    const token = localStorage.getItem('token');
    if (!token) return;
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get<any[]>(`${environment.apiUrl}/pagos/mi-historial`, { headers }).subscribe({
      next: (pagos) => {
        const pagosCompletados = pagos.filter(p => p.estado === 'completado');
        
        // 🚩 SOLUCIÓN: Usamos limpiarNumero para evitar la concatenación de strings
        this.estadisticasFinanzas.totalBruto = pagosCompletados.reduce((sum: number, p: any) => sum + this.limpiarNumero(p.monto), 0);
        this.estadisticasFinanzas.totalComision = pagosCompletados.reduce((sum: number, p: any) => sum + this.limpiarNumero(p.comision_plataforma), 0);
        this.estadisticasFinanzas.totalNeto = this.estadisticasFinanzas.totalBruto - this.estadisticasFinanzas.totalComision;
        
        this.estadisticasFinanzas.cantidadPagos = pagosCompletados.length;
        this.estadisticasFinanzas.cargando = false;
      },
      error: () => {
        this.estadisticasFinanzas.cargando = false;
      }
    });
  }

  // 🚩 FUNCIÓN SALVAVIDAS: Convierte textos corruptos en números reales
  limpiarNumero(valor: any): number {
    if (!valor) return 0;
    const numero = parseFloat(valor);
    return isNaN(numero) ? 0 : numero;
  }
}