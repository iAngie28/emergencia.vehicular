import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
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
  private cdr = inject(ChangeDetectorRef);
  
  vistaActual: 'admins' | 'tecnicos' | 'especialidades' = 'admins'; 
  
  admins: any[] = [];
  tecnicos: any[] = [];
  especialidades: any[] = []; 
  usuariosFiltrados: any[] = []; 

  nuevoUsuario: any = this.getUsuarioBase();
  nuevaEspecialidad = { nombre: '', descripcion: '' };
  editandoId: number | null = null;

  filtroEspecialidad: string = '';
  mostrarDropdown: boolean = false;

  ngOnInit() { 
    this.cargarCatalogos();
    this.refrescarTodo();
  }

  getUsuarioBase() {
    return { nombre: '', correo: '', clave: '', telefono: '', esta_activo: true, especialidades_ids: [] };
  }

  cargarCatalogos() {
    this.usuariosService.getEspecialidades().subscribe({
      next: (data) => this.especialidades = data,
      error: (e) => console.error('Error especialidades:', e)
    });
  }

  refrescarTodo() {
    this.usuariosService.getMisAdmins().subscribe(data => {
      this.admins = data;
      if (this.vistaActual === 'admins') this.actualizarTabla();
    });
    this.usuariosService.getMisTecnicos().subscribe(data => {
      this.tecnicos = data;
      if (this.vistaActual === 'tecnicos') this.actualizarTabla();
    });
  }

  cambiarVista(vista: 'admins' | 'tecnicos' | 'especialidades') {
    this.vistaActual = vista;
    this.cancelarEdicion();
    if (vista !== 'especialidades') {
      this.actualizarTabla();
    }
  }

  actualizarTabla() {
    const fuente = this.vistaActual === 'admins' ? this.admins : this.tecnicos;
    this.usuariosFiltrados = [...fuente];
    this.cdr.detectChanges();
  }

  // --- GESTIÓN DE ESPECIALIDADES ---
  guardarEspecialidad() {
    if (!this.nuevaEspecialidad.nombre) return alert('El nombre es obligatorio');
    this.usuariosService.crearEspecialidad(this.nuevaEspecialidad).subscribe({
      next: () => {
        alert('Especialidad añadida al catálogo ✅');
        this.nuevaEspecialidad = { nombre: '', descripcion: '' };
        this.cargarCatalogos();
      },
      error: (e) => alert(this.obtenerMensajeError(e))
    });
  }

  borrarEspecialidad(id: number) {
    if (confirm('¿Eliminar esta especialidad del catálogo global?')) {
      this.usuariosService.eliminarEspecialidad(id).subscribe({
        next: () => this.cargarCatalogos(),
        error: (e) => alert('No se puede eliminar: posiblemente está asignada a un técnico.')
      });
    }
  }

  // --- TRADUCCIÓN DE ERRORES ---
  private obtenerMensajeError(error: any): string {
    if (error.error && error.error.detail) {
      if (Array.isArray(error.error.detail)) {
        return error.error.detail.map((err: any) => `⚠️ ${err.loc[err.loc.length - 1]}: ${err.msg}`).join('\n');
      }
      return `⚠️ ${error.error.detail}`;
    }
    return '❌ Error de conexión.';
  }

  // --- LÓGICA DE USUARIOS Y CHIPS ---
  get especialidadesFiltradas() {
    return this.especialidades.filter(esp => 
      esp.nombre.toLowerCase().includes(this.filtroEspecialidad.toLowerCase()) &&
      !this.nuevoUsuario.especialidades_ids.includes(esp.id)
    );
  }

  get especialidadesSeleccionadas() {
    return this.especialidades.filter(esp => this.nuevoUsuario.especialidades_ids.includes(esp.id));
  }

  toggleEspecialidad(id: number) {
    const index = this.nuevoUsuario.especialidades_ids.indexOf(id);
    if (index > -1) this.nuevoUsuario.especialidades_ids.splice(index, 1);
    else this.nuevoUsuario.especialidades_ids.push(id);
  }

  prepararEdicion(usuario: any) {
    this.editandoId = usuario.id;
    const espIds = usuario.especialidades ? usuario.especialidades.map((e: any) => e.id) : [];
    this.nuevoUsuario = { ...usuario, clave: '', especialidades_ids: espIds, esta_activo: usuario.esta_activo ?? true };
  }

  cancelarEdicion() {
    this.editandoId = null;
    this.nuevoUsuario = this.getUsuarioBase();
    this.filtroEspecialidad = '';
    this.mostrarDropdown = false;
  }

  guardar() {
    const data = { ...this.nuevoUsuario };
    if (!data.clave || data.clave.trim() === '') delete data.clave;

    const peticion = this.vistaActual === 'admins' 
      ? (this.editandoId ? this.usuariosService.actualizarAdmin(this.editandoId, data) : this.usuariosService.crearColega(data))
      : (this.editandoId ? this.usuariosService.actualizarTecnico(this.editandoId, data) : this.usuariosService.crearTecnico(data));

    peticion.subscribe({
      next: () => {
        alert('Guardado con éxito ✅');
        this.cancelarEdicion();
        this.refrescarTodo();
      },
      error: (e) => alert(this.obtenerMensajeError(e))
    });
  }

  borrar(id: number) {
    if (confirm('¿Eliminar este usuario?')) {
      this.usuariosService.eliminarAdmin(id).subscribe({
        next: () => this.refrescarTodo(),
        error: (e) => alert('Error al eliminar')
      });
    }
  }
}