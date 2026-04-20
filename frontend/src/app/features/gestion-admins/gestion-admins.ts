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
    // 1. Validación de longitud de contraseña
    if (!this.editandoId || (this.nuevoAdmin.clave && this.nuevoAdmin.clave.trim() !== '')) {
      if (this.nuevoAdmin.clave.length < 8) {
        alert('La contraseña debe tener al menos 8 caracteres. 🔐');
        return;
      }
    }

    const data: any = {
      nombre: this.nuevoAdmin.nombre,
      correo: this.nuevoAdmin.correo,
      telefono: this.nuevoAdmin.telefono,
    };

    if (this.editandoId) {
      // --- ACTUALIZACIÓN ---
      if (this.nuevoAdmin.clave && this.nuevoAdmin.clave.trim() !== '') {
        data.clave_hash = this.nuevoAdmin.clave;
      }

      this.usuariosService.actualizarAdmin(this.editandoId, data).subscribe({
        next: (adminActualizado) => {
          alert('¡Datos del colega actualizados! ✅');
          
          // ACTUALIZACIÓN REACTIVA: Buscamos en la lista y reemplazamos los datos
          this.admins = this.admins.map(a => a.id === this.editandoId ? { ...a, ...data } : a);
          
          this.cancelarEdicion();
        },
        error: (e) => this.mostrarError(e)
      });
    } else {
      // --- REGISTRO NUEVO ---
      data.clave_hash = this.nuevoAdmin.clave; 
      data.rol_id = 1; 
      
      this.usuariosService.crearColega(data).subscribe({
        next: (nuevoAdminCreado) => { 
          alert('¡Administrador Registrado con éxito! 🎉');
          
          // ACTUALIZACIÓN REACTIVA: Metemos al nuevo admin al principio de la lista
          // Usamos lo que nos devuelve el servidor (nuevoAdminCreado) para tener el ID real
          this.admins = [nuevoAdminCreado, ...this.admins];
          
          this.cancelarEdicion();
        },
        error: (e) => this.mostrarError(e)
      });
    }
  }

  // Función auxiliar para extraer el mensaje de error y evitar el [object Object]
  private mostrarError(e: any) {
    let mensaje = 'Ocurrió un error inesperado';
    
    if (e.error && e.error.detail) {
      if (Array.isArray(e.error.detail)) {
        // Errores de validación de FastAPI suelen ser una lista
        mensaje = e.error.detail[0].msg || 'Error de validación en los datos';
      } else {
        mensaje = e.error.detail;
      }
    }
    
    alert(mensaje);
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