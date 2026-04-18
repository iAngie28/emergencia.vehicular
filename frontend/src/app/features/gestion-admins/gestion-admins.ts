import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UsuariosService } from '../../core/services/usuarios';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './gestion-admins.html'
})
export class GestionAdminsComponent implements OnInit {
  private usuariosService = inject(UsuariosService);
  
  admins: any[] = [];
  nuevoAdmin = { nombre: '', correo: '', clave: '' };

  ngOnInit() { 
    this.cargarAdmins(); 
  }

  cargarAdmins() {
    this.usuariosService.getMisAdmins().subscribe({
      next: (data) => this.admins = data,
      error: (e) => console.error('Error al cargar admins:', e)
    });
  }

  registrar() {
    this.usuariosService.crearColega(this.nuevoAdmin).subscribe({
      // 🚩 Agregamos 'res' (o el nombre que quieras) aquí:
      next: (res) => { 
        alert('¡Administrador Registrado! 🎉');
        this.nuevoAdmin = { nombre: '', correo: '', clave: '' };
        
        // 🚩 Ahora usamos 'res', que contiene los datos del nuevo admin
        this.admins = [...this.admins, res];
        
        this.cargarAdmins();
      },
      error: (e) => alert(e.error?.detail || 'Error al registrar')
    });
  }

  borrar(id: number) {
    if (confirm('¿Seguro que quieres quitar a este administrador?')) {
      this.usuariosService.eliminarAdmin(id).subscribe({
        next: () => {
          // 🚩 Esto avisa que salió bien y recarga la lista
          alert('Administrador eliminado correctamente.');
          this.admins = this.admins.filter(admin => admin.id !== id);
          this.cargarAdmins();
        },
        error: (e) => {
          // 🚩 Esto te avisará cuando intentes borrarte a ti misma
          // o si ocurre cualquier otro error del backend
          alert(e.error?.detail || 'No se pudo eliminar al usuario');
          this.cargarAdmins(); // Recargamos por si acaso
        }
      });
    }
  }
}