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
}