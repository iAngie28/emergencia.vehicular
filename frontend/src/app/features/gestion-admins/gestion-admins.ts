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

    // 🚩 REVISIÓN DE CAMPO: Mapeamos 'clave' a 'password' para el Backend
    // Si tu modelo pide 'password', esto soluciona el error de validación.
    if (data.clave) {
      data.password = data.clave;
      delete data.clave;
    }

    if (this.editandoId) {
      // MODO EDICIÓN
      if (!data.password || data.password.trim() === '') {
        delete data.password;
      }

      this.usuariosService.actualizarAdmin(this.editandoId, data).subscribe({
        next: () => {
          alert('¡Datos del colega actualizados! ✅');
          this.cancelarEdicion();
          this.cargarAdmins(); // 🔄 Recarga la tabla
        },
        error: (e) => this.mostrarError(e) // 🧐 Manejo de errores detallado
      });
    } else {
      // MODO REGISTRO NUEVO
      data.rol_id = 1;
      
      this.usuariosService.crearColega(data).subscribe({
        next: () => { 
          alert('¡Administrador Registrado! 🎉');
          this.cancelarEdicion();
          this.cargarAdmins(); // 🔄 Recarga la tabla
        },
        error: (e) => this.mostrarError(e) // 🧐 Manejo de errores detallado
      });
    }
  }

  // 👇 NUEVA FUNCIÓN: Para que no salga [object Object]
  private mostrarError(e: any) {
    console.error(e);
    let mensaje = 'Ocurrió un error inesperado';

    if (e.error && e.error.detail) {
      // Si FastAPI devuelve una lista de errores de validación (Pydantic)
      if (Array.isArray(e.error.detail)) {
        mensaje = e.error.detail.map((err: any) => {
          // Extrae el campo (ej: password) y el mensaje (ej: too short)
          const campo = err.loc[err.loc.length - 1];
          return `${campo}: ${err.msg}`;
        }).join('\n');
      } else {
        // Si es un string simple
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