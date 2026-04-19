import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-finanzas',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './finanzas.html',
  styleUrl: './finanzas.css'
})
export class FinanzasComponent implements OnInit {
  private http = inject(HttpClient);
  
  pagosHistorial: any[] = [];
  cargando: boolean = false;

  pagoSeleccionado: any = null;
  pagoEditado: any = {}; 

  ngOnInit() {
    this.cargarPagos();
  }

  cargarPagos() {
    this.cargando = true;
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get<any[]>('http://localhost:8000/api/v1/pagos/mi-historial', { headers }).subscribe({
      next: (data) => {
        // 🚩 ORDENAMIENTO: Forzamos a que los IDs más altos (más nuevos) salgan primero
        this.pagosHistorial = data.sort((a, b) => b.id - a.id);
        this.cargando = false;
      },
      error: () => this.cargando = false
    });
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
    
    // Empaquetamos los datos editados
    const payload = {
      monto: this.pagoEditado.monto,
      metodo_pago: this.pagoEditado.metodo_pago,
      estado: this.pagoEditado.estado
    };

    // Llamamos al nuevo endpoint PUT
    this.http.put(`http://localhost:8000/api/v1/pagos/${this.pagoEditado.id}`, payload, { headers }).subscribe({
      next: () => {
        alert('¡Cambios guardados con éxito! 💾');
        
        // 1. Actualizamos la tabla reactivamente
        this.pagosHistorial = this.pagosHistorial.map(p => 
          p.id === this.pagoEditado.id ? { ...p, ...payload } : p
        );

        // 2. Actualizamos el panel lateral actual. 
        // Si el estado cambió a 'completado' o 'cancelado', la vista se transformará en el "Recibo de Solo Lectura" instantáneamente.
        this.pagoSeleccionado = { ...this.pagoSeleccionado, ...payload };
      },
      error: (err) => alert('Error al guardar: ' + err.error?.detail)
    });
  }

  confirmarPago(pagoId: number) {
    if (!confirm('¿Confirmar que el dinero ya está en tus manos o cuenta?')) return;
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.put(`http://localhost:8000/api/v1/pagos/${pagoId}/confirmar`, {}, { headers }).subscribe({
      next: () => {
        // 🚩 ACTUALIZACIÓN REACTIVA: Cambiamos la tabla al instante
        this.pagosHistorial = this.pagosHistorial.map(p => 
          p.id === pagoId ? { ...p, estado: 'completado' } : p
        );

        // Si el panel lateral está abierto, también actualizamos su estado para que cambie a "Solo lectura"
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
    
    this.http.put(`http://localhost:8000/api/v1/pagos/${pagoId}/cancelar`, {}, { headers }).subscribe({
      next: () => {
        // 🚩 ACTUALIZACIÓN REACTIVA: Cambiamos la tabla al instante
        this.pagosHistorial = this.pagosHistorial.map(p => 
          p.id === pagoId ? { ...p, estado: 'cancelado' } : p
        );

        // Actualizamos el panel lateral para que muestre el bloqueo rojo
        if (this.pagoSeleccionado?.id === pagoId) {
          this.pagoSeleccionado = { ...this.pagoSeleccionado, estado: 'cancelado' };
        }
      },
      error: (err) => alert('Error al cancelar: ' + err.error?.detail)
    });
  }
}