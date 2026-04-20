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
    // 1. Validación de longitud de contraseña (mínimo 8 caracteres)
    if (!this.editandoId || (this.nuevoAdmin.clave && this.nuevoAdmin.clave.trim() !== '')) {
      if (this.nuevoAdmin.clave.length < 8) {
        alert('La contraseña debe tener al menos 8 caracteres. 🔐');
        return;
      }
    }

    // 2. Preparamos el objeto exacto que espera el Backend (mapeando clave -> password)
    const data: any = {
      nombre: this.nuevoAdmin.nombre,
      correo: this.nuevoAdmin.correo,
      telefono: this.nuevoAdmin.telefono,
    };

    if (this.editandoId) {
      // --- LÓGICA DE ACTUALIZACIÓN ---
      if (this.nuevoAdmin.clave && this.nuevoAdmin.clave.trim() !== '') {
        data.password = this.nuevoAdmin.clave;
      }

      this.usuariosService.actualizarAdmin(this.editandoId, data).subscribe({
        next: () => {
          alert('¡Datos del colega actualizados! ✅');
          this.cancelarEdicion();
          this.cargarAdmins();
        },
        error: (e) => {
          console.error('Error PUT:', e);
          this.mostrarError(e);
        }
      });
    } else {
      // --- LÓGICA DE REGISTRO NUEVO ---
      data.password = this.nuevoAdmin.clave; 
      data.rol_id = 1; // Administrador de Taller
      
      this.usuariosService.crearColega(data).subscribe({
        next: () => { 
          alert('¡Administrador Registrado con éxito! 🎉');
          this.cancelarEdicion();
          this.cargarAdmins();
        },
        error: (e) => {
          console.error('Error POST:', e);
          this.mostrarError(e);
        }
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