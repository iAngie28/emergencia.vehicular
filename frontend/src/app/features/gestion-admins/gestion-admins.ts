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

  private obtenerMensajeError(error: any): string {
    // Si es un objeto con propiedades de campos, mostrar el campo específico
    if (error.error && typeof error.error === 'object') {
      // Si tiene 'detail', lo mostramos
      if (error.error.detail) {
        return error.error.detail;
      }
      // Si tiene estructura de errores por campo
      if (error.error.errors || error.error.field_errors) {
        const errores = error.error.errors || error.error.field_errors;
        const campos = Object.keys(errores);
        if (campos.length > 0) {
          return `Campo inválido: ${campos[0]} - ${errores[campos[0]]}`;
        }
      }
      // Si no, intentar obtener la primera clave-valor
      const claves = Object.keys(error.error);
      if (claves.length > 0 && claves[0] !== 'detail') {
        return `${claves[0]}: ${error.error[claves[0]]}`;
      }
    }
    return 'Error desconocido';
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
        error: (e) => alert(this.obtenerMensajeError(e))
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
        error: (e) => alert(this.obtenerMensajeError(e))
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