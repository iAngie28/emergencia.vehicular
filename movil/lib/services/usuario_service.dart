import 'api_service.dart';

/// Servicio de usuario para funcionalidades expuestas al cliente movil.
class UsuarioService {
  final ApiService apiService;

  UsuarioService({required this.apiService});

  Future<Map<String, dynamic>> obtenerPerfil() async {
    try {
      final response = await apiService.get('/api/v1/usuarios/me');

      if (response is Map<String, dynamic>) {
        return response;
      }
      throw Exception('Respuesta inesperada del servidor');
    } catch (e) {
      throw Exception('Error al obtener perfil: $e');
    }
  }

  /// Endpoint de actualizacion disponible para administradores de taller.
  /// En movil cliente esta funcionalidad queda deshabilitada por backend.
  Future<Map<String, dynamic>> actualizarPerfilNoDisponible() async {
    throw Exception(
      'Actualizar perfil no disponible para rol movil en backend actual.',
    );
  }

  Future<Map<String, dynamic>> solicitarRecuperacionContrasena({
    required String correo,
  }) async {
    try {
      final response = await apiService.post(
        '/api/v1/auth/forgot-password',
        body: {'correo': correo},
      );

      if (response is Map<String, dynamic>) {
        return response;
      }
      throw Exception('Respuesta inesperada del servidor');
    } catch (e) {
      throw Exception('Error al solicitar recuperacion de contrasena: $e');
    }
  }
}
