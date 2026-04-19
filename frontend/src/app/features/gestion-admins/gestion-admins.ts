import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UsuariosService } from '../../core/services/usuarios';

@Component({
  selector: 'app-gestion-admins',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './gestion-admins.html',
  styleUrl: './gestion-admins.css'
})
export class GestionAdminsComponent implements OnInit {
  private usuariosService = inject(UsuariosService);
  
  admins: any[] = [];
  nuevoAdmin: any = { 
    nombre: '', 
    correo: '', 
    clave: '', 
    telefono: '' 
  };
  editandoId: number | null = null;

  ngOnInit() { 
    this.cargarAdmins(); 
  }

  cargarAdmins() {
    this.usuariosService.getMisAdmins().subscribe({
      next: (data) => this.admins = data,
      error: (e) => console.error('Error al cargar admins:', e)
    });
  }

  prepararEdicion(admin: any) {
    this.editandoId = admin.id;
    // Clonamos el objeto y reseteamos la clave para el formulario
    this.nuevoAdmin = { ...admin, clave: '' };
  }

  cancelarEdicion() {
    this.editandoId = null;
    this.nuevoAdmin = { 
      nombre: '', 
      correo: '', 
      clave: '', 
      telefono: '' 
    };
  }

  guardar() {
    // 🛡️ Clonamos los datos para procesarlos antes de enviar
    const data = { ...this.nuevoAdmin };

    if (this.editandoId) {
      // 🔍 FIX QA: Si la clave está vacía en edición, la eliminamos del objeto
      // para que el backend no intente validarla (evita el error 422)
      if (!data.clave || data.clave.trim() === '') {
        delete data.clave;
      }

      this.usuariosService.actualizarAdmin(this.editandoId, data).subscribe({
        next: () => {
          alert('¡Datos del colega actualizados! ✅');
          this.cancelarEdicion();
          this.cargarAdmins();
        },
        error: (e) => alert(e.error?.detail || 'Error al actualizar')
      });
    } else {
      // 🚀 REGISTRAR NUEVO: Forzamos el rol de Administrador de Taller (ID: 1)
      data.rol_id = 1;
      
      this.usuariosService.crearColega(data).subscribe({
        next: () => { 
          alert('¡Administrador Registrado y vinculado a tu taller! 🎉');
          this.cancelarEdicion();
          this.cargarAdmins();
        },
        error: (e) => alert(e.error?.detail || 'Error al registrar')
      });
    }
  }

  borrar(id: number) {
    if (confirm('¿Seguro que quieres quitar a este administrador de tu equipo?')) {
      this.usuariosService.eliminarAdmin(id).subscribe({
        next: () => {
          this.admins = this.admins.filter(admin => admin.id !== id);
          alert('Eliminado con éxito');
        },
        error: (e) => alert(e.error?.detail || 'No se pudo eliminar')
      });
    }
  }
}