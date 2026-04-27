import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { HttpClient, HttpHeaders } from '@angular/common/http';
// 👇 1. Importamos el environment global
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-finanzas',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './finanzas.html',
  styleUrl: './finanzas.css'
})
export class FinanzasComponent implements OnInit {
  private http = inject(HttpClient);
  // 👇 2. Definimos la base URL usando el environment
  private apiUrl = `${environment.apiUrl}/pagos`;
  
  pagosHistorial: any[] = [];
  cargando: boolean = false;

  pagoSeleccionado: any = null;
  pagoEditado: any = {};
  
  // KPIs Financieros
  estadisticas: any = {
    totalBruto: 0,
    totalComision: 0,
    totalNeto: 0,
    cantidadPagos: 0
  }; 

  ngOnInit() {
    this.cargarPagos();
    this.calcularEstadisticas();
  }

  cargarPagos() {
    this.cargando = true;
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    // 👇 3. Cambiado localhost por this.apiUrl
    this.http.get<any[]>(`${this.apiUrl}/mi-historial`, { headers }).subscribe({
      next: (data) => {
        this.pagosHistorial = data.sort((a, b) => b.id - a.id);
        this.calcularEstadisticas();
        this.cargando = false;
      },
      error: () => this.cargando = false
    });
  }

  calcularEstadisticas() {
    const pagosCompletados = this.pagosHistorial.filter(p => p.estado === 'completado');
    
    this.estadisticas.totalBruto = pagosCompletados.reduce((sum: number, p: any) => sum + (p.monto || 0), 0);
    this.estadisticas.totalComision = pagosCompletados.reduce((sum: number, p: any) => sum + (p.comision_plataforma || 0), 0);
    this.estadisticas.totalNeto = this.estadisticas.totalBruto - this.estadisticas.totalComision;
    this.estadisticas.cantidadPagos = pagosCompletados.length;
  }

  verDetalle(pago: any) {
    this.pagoSeleccionado = pago;
    this.pagoEditado = { ...pago };
  }

  cerrarDetalle() {
    this.pagoSeleccionado = null;
    this.pagoEditado = {};
  }

  guardarCambios() {
    if (this.pagoEditado.monto <= 0) return alert('El monto debe ser mayor a 0');

    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    const payload = {
      monto: this.pagoEditado.monto,
      metodo_pago: this.pagoEditado.metodo_pago,
      estado: this.pagoEditado.estado
    };

    // 👇 4. Cambiado localhost por this.apiUrl
    this.http.put(`${this.apiUrl}/${this.pagoEditado.id}`, payload, { headers }).subscribe({
      next: () => {
        alert('¡Cambios guardados con éxito! 💾');
        this.pagosHistorial = this.pagosHistorial.map(p => 
          p.id === this.pagoEditado.id ? { ...p, ...payload } : p
        );
        this.pagoSeleccionado = { ...this.pagoSeleccionado, ...payload };
      },
      error: (err) => alert('Error al guardar: ' + err.error?.detail)
    });
  }

  confirmarPago(pagoId: number) {
    if (!confirm('¿Confirmar que el dinero ya está en tus manos o cuenta?')) return;
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    // 👇 5. Cambiado localhost por this.apiUrl
    this.http.put(`${this.apiUrl}/${pagoId}/confirmar`, {}, { headers }).subscribe({
      next: () => {
        this.pagosHistorial = this.pagosHistorial.map(p => 
          p.id === pagoId ? { ...p, estado: 'completado' } : p
        );
        if (this.pagoSeleccionado?.id === pagoId) {
          this.pagoSeleccionado = { ...this.pagoSeleccionado, estado: 'completado' };
        }
      },
      error: (err) => alert('Error al confirmar pago: ' + err.error?.detail)
    });
  }

  cancelarPago(pagoId: number) {
    if (!confirm('¿Seguro que deseas anular/revertir este cobro?')) return;
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    // 👇 6. Cambiado localhost por this.apiUrl
    this.http.put(`${this.apiUrl}/${pagoId}/cancelar`, {}, { headers }).subscribe({
      next: () => {
        this.pagosHistorial = this.pagosHistorial.map(p => 
          p.id === pagoId ? { ...p, estado: 'cancelado' } : p
        );
        if (this.pagoSeleccionado?.id === pagoId) {
          this.pagoSeleccionado = { ...this.pagoSeleccionado, estado: 'cancelado' };
        }
      },
      error: (err) => alert('Error al cancelar: ' + err.error?.detail)
    });
  }
}