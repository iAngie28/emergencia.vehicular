

export interface TecnicoInfo {
  id: number;
  nombre: string;
}

export interface Incidente {
  id: number;
  vehiculo_id: number;
  usuario_id: number;
  taller_id?: number;
  tecnico_id?: number;
  latitud: number;
  longitud: number;
  prioridad: string;
  estado: string;
  pago_estado: string;
  telefono_cliente?: string;
  motivo_cancelacion?: string;
  transcripcion_audio?: string;
  clasificacion_ia?: string;
  resumen_ia?: string;
  fecha_creacion?: string; // Campo vital para el historial
  tecnico?: TecnicoInfo;    // Relación para mostrar quién atendió
  pagos?: any;              // Relación con pagos (monto cobrado)
  descargando?: boolean;
}