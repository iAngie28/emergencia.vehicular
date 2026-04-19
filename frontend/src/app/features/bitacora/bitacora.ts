import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BitacoraService, BitacoraEntry } from '../../core/services/bitacora.service';

@Component({
  selector: 'app-bitacora',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './bitacora.html',
  styleUrls: ['./bitacora.css']
})
export class BitacoraComponent implements OnInit {
  private bitacoraService = inject(BitacoraService);
  logs: BitacoraEntry[] = [];

  ngOnInit() {
    this.bitacoraService.getLogs().subscribe({
      next: (data) => this.logs = data,
      error: (err) => console.error('Error en bitácora:', err)
    });
  }

  // Helper puramente visual para colorear las etiquetas según la acción
  getBadgeColor(accion: string): string {
    if (!accion) return 'badge-default';
    const act = accion.toUpperCase();
    
    if (act.includes('CREAR') || act.includes('GENERAR')) return 'badge-success';
    if (act.includes('ACTUALIZAR') || act.includes('CONFIRMAR') || act.includes('EDITAR')) return 'badge-info';
    if (act.includes('ELIMINAR') || act.includes('CANCELAR')) return 'badge-danger';
    
    return 'badge-default';
  }
}