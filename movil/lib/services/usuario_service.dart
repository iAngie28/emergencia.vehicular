import 'package:http/http.dart' as http;
import 'api_service.dart';

/// Servicio para gestionar la información del usuario
class UsuarioService {
  final ApiService apiService;

  UsuarioService({required this.apiService});

  /// Obtener perfil del usuario actual
  /// GET /api/v1/usuarios/me
  Future<Map<String, dynamic>> obtenerPerfil() async {
    try {
      final response = await apiService.get('/api/v1/usuarios/me');

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al obtener perfil: $e');
    }
  }

  /// Actualizar información del usuario
  /// PUT /api/v1/usuarios/me
  Future<Map<String, dynamic>> actualizarPerfil({
    String? nombre,
    String? apellido,
    String? telefono,
    String? direccion,
    String? ciudad,
  }) async {
    try {
      final body = {
        if (nombre != null) 'nombre': nombre,
        if (apellido != null) 'apellido': apellido,
        if (telefono != null) 'telefono': telefono,
        if (direccion != null) 'direccion': direccion,
        if (ciudad != null) 'ciudad': ciudad,
      };

      final response = await apiService.put(
        '/api/v1/usuarios/me',
        body: body,
      );

      return response;
    } catch (e) {
      throw Exception('Error al actualizar perfil: $e');
    }
  }

  /// Cambiar contraseña
  /// POST /api/v1/usuarios/cambiar-contraseña
  Future<Map<String, dynamic>> cambiarContrasena({
    required String contrasenaActual,
    required String contrasenaNueva,
  }) async {
    try {
      final response = await apiService.post(
        '/api/v1/usuarios/cambiar-contraseña',
        body: {
          'contraseña_actual': contrasenaActual,
          'contraseña_nueva': contrasenaNueva,
        },
      );

      return response;
    } catch (e) {
      throw Exception('Error al cambiar contraseña: $e');
    }
  }

  /// Solicitar recuperación de contraseña
  /// POST /api/v1/usuarios/recuperar-contraseña
  Future<Map<String, dynamic>> solicitarRecuperacionContrasena({
    required String email,
  }) async {
    try {
      final response = await apiService.post(
        '/api/v1/usuarios/recuperar-contraseña',
        body: {
          'email': email,
        },
      );

      return response;
    } catch (e) {
      throw Exception('Error al solicitar recuperación de contraseña: $e');
    }
  }

  /// Obtener un usuario por ID (principalmente para talleres)
  /// GET /api/v1/usuarios/{id}
  Future<Map<String, dynamic>> obtenerUsuario({required int usuarioId}) async {
    try {
      final response = await apiService.get('/api/v1/usuarios/$usuarioId');

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al obtener usuario: $e');
    }
  }

  /// Verificar si existe un usuario por email
  /// GET /api/v1/usuarios/verificar-email?email={email}
  Future<bool> verificarEmail({required String email}) async {
    try {
      final response = await apiService.get(
        '/api/v1/usuarios/verificar-email',
        queryParams: {'email': email},
      );

      if (response is Map<String, dynamic> && response['existe'] != null) {
        return response['existe'] as bool;
      }
      return false;
    } catch (e) {
      throw Exception('Error al verificar email: $e');
    }
  }
}
