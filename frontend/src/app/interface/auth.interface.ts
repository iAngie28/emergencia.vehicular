/**
 * Define la estructura de la respuesta del servidor al hacer login o registro
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

/**
 * Define la estructura del Taller que se crea durante el onboarding
 */
export interface TallerRegistro {
  nombre: string;
  direccion: string;
  latitud: number;
  longitud: number;
  comision_porcentaje: number;
}

/**
 * Define el paquete completo: Datos del Usuario + Datos de su Taller
 * Este es el molde que usa el formulario de registro
 */
export interface RegistroSaaS {
  nombre: string;
  correo: string;
  password: string;
  taller: TallerRegistro;
}