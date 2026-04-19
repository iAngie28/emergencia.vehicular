import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'api_service.dart';

/// Servicio para gestionar incidentes del usuario
class IncidenteService {
  final ApiService apiService;

  IncidenteService({required this.apiService});

  /// Reportar un nuevo incidente (Cliente)
  /// POST /api/v1/incidentes/
  Future<Map<String, dynamic>> reportarIncidente({
    required int usuarioId,
    required int vehiculoId,
    required String descripcion,
    required String ubicacion,
    required double latitud,
    required double longitud,
  }) async {
    try {
      final response = await apiService.post(
        '/api/v1/incidentes/',
        body: {
          'usuario_id': usuarioId,
          'vehiculo_id': vehiculoId,
          'descripcion': descripcion,
          'ubicacion': ubicacion,
          'latitud': latitud,
          'longitud': longitud,
          'estado': 'pendiente',
        },
      );

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al reportar incidente: $e');
    }
  }

  /// Obtener mis incidentes reportados (Cliente)
  /// GET /api/v1/incidentes/mis-reportes?usuario_id={id}
  Future<List<Map<String, dynamic>>> obtenerMisIncidentes({
    required int usuarioId,
  }) async {
    try {
      final response = await apiService.get(
        '/api/v1/incidentes/mis-reportes',
        queryParams: {'usuario_id': usuarioId},
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
      throw Exception('Error al obtener mis incidentes: $e');
    }
  }

  /// Obtener un incidente específico
  /// GET /api/v1/incidentes/{id}
  Future<Map<String, dynamic>> obtenerIncidente({required int id}) async {
    try {
      final response = await apiService.get('/api/v1/incidentes/$id');

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al obtener incidente: $e');
    }
  }

  /// Adjuntar evidencia (foto/archivo) a un incidente
  /// POST /api/v1/incidentes/{id}/evidencia
  Future<Map<String, dynamic>> adjuntarEvidencia({
    required int incidenteId,
    required String rutaArchivo,
    required String tipo, // 'foto', 'video', 'documento'
  }) async {
    try {
      // Lee el archivo y lo convierte a bytes
      final file = File(rutaArchivo);
      final bytes = await file.readAsBytes();
      final base64 = base64Encode(bytes);

      final response = await apiService.post(
        '/api/v1/incidentes/$incidenteId/evidencia',
        body: {
          'archivo_base64': base64,
          'tipo': tipo,
          'nombre': file.path.split('/').last,
        },
      );

      return response;
    } catch (e) {
      throw Exception('Error al adjuntar evidencia: $e');
    }
  }

  /// Obtener el estado actual de un incidente
  /// GET /api/v1/incidentes/{id}/estado
  Future<Map<String, dynamic>> obtenerEstadoIncidente({required int id}) async {
    try {
      final response = await apiService.get('/api/v1/incidentes/$id/estado');

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al obtener estado del incidente: $e');
    }
  }

  /// Listar incidentes pendientes cercanos (FUTURO: requiere geolocalización)
  /// GET /api/v1/incidentes/pendientes
  /// TODO: Esta funcionalidad requiere implementar:
  /// - Servicios de geolocalización
  /// - Cálculo de distancia entre usuario y incidentes
  /// - Filtrado por proximidad
  /// - Sistema de notificaciones para nuevos incidentes cercanos
  Future<List<Map<String, dynamic>>> obtenerIncidentesPendientesCercanos() async {
    try {
      print('⚠️ ACTUALIZACIÓN NO DISPONIBLE: La funcionalidad de talleres cercanos');
      print('se implementará en la próxima versión con servicios de geolocalización.');
      return [];
    } catch (e) {
      throw Exception('Error al obtener incidentes cercanos: $e');
    }
  }
}
