import 'package:http/http.dart' as http;
import 'api_service.dart';

/// Servicio para gestionar notificaciones del usuario
class NotificacionService {
  final ApiService apiService;

  NotificacionService({required this.apiService});

  /// Registrar el token de Firebase Cloud Messaging (FCM)
  /// POST /api/v1/notificaciones/tokens
  Future<Map<String, dynamic>> registrarTokenDispositivo({
    required int usuarioId,
    required String tokenFCM,
    required String plataforma, // 'android' o 'ios'
  }) async {
    try {
      final response = await apiService.post(
        '/api/v1/notificaciones/tokens',
        body: {
          'usuario_id': usuarioId,
          'token_fcm': tokenFCM,
          'plataforma': plataforma,
          'activo': true,
        },
      );

      return response;
    } catch (e) {
      throw Exception('Error al registrar token de dispositivo: $e');
    }
  }

  /// Obtener notificaciones no leídas del usuario
  /// GET /api/v1/notificaciones/usuario/{usuario_id}/pendientes
  Future<List<Map<String, dynamic>>> obtenerNotificacionesNoLeidas({
    required int usuarioId,
  }) async {
    try {
      final response = await apiService.get(
        '/api/v1/notificaciones/usuario/$usuarioId/pendientes',
      );

      if (response is List) {
        return List<Map<String, dynamic>>.from(
          response.map((item) => item as Map<String, dynamic>)
        );
      } else if (response is Map<String, dynamic>) {
        return [response];
      } else {
        throw Exception('Formato de respuesta inesperado');
      }
    } catch (e) {
      throw Exception('Error al obtener notificaciones: $e');
    }
  }

  /// Marcar una notificación como leída
  /// PATCH /api/v1/notificaciones/{id}/leer
  Future<Map<String, dynamic>> marcarComoLeida({
    required int notificacionId,
  }) async {
    try {
      final response = await apiService.patch(
        '/api/v1/notificaciones/$notificacionId/leer',
      );

      return response;
    } catch (e) {
      throw Exception('Error al marcar notificación como leída: $e');
    }
  }

  /// Obtener todas las notificaciones (leídas y no leídas)
  /// GET /api/v1/notificaciones/usuario/{usuario_id}/historial
  Future<List<Map<String, dynamic>>> obtenerHistorialNotificaciones({
    required int usuarioId,
  }) async {
    try {
      final response = await apiService.get(
        '/api/v1/notificaciones/usuario/$usuarioId/historial',
      );

      if (response is List) {
        return List<Map<String, dynamic>>.from(
          response.map((item) => item as Map<String, dynamic>)
        );
      } else if (response is Map<String, dynamic>) {
        return [response];
      } else {
        throw Exception('Formato de respuesta inesperado');
      }
    } catch (e) {
      throw Exception('Error al obtener historial de notificaciones: $e');
    }
  }

  /// Eliminar una notificación
  /// DELETE /api/v1/notificaciones/{id}
  Future<Map<String, dynamic>> eliminarNotificacion({
    required int notificacionId,
  }) async {
    try {
      final response = await apiService.delete(
        '/notificaciones/$notificacionId',
      );

      return response;
    } catch (e) {
      throw Exception('Error al eliminar notificación: $e');
    }
  }

  /// Desactivar el token de dispositivo (cuando el usuario cierra sesión)
  /// PATCH /api/v1/notificaciones/tokens/{token}/desactivar
  Future<Map<String, dynamic>> desactivarTokenDispositivo({
    required String tokenFCM,
  }) async {
    try {
      final response = await apiService.patch(
        '/notificaciones/tokens/$tokenFCM/desactivar',
      );

      return response;
    } catch (e) {
      throw Exception('Error al desactivar token: $e');
    }
  }
}
