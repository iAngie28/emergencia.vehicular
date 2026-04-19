import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_service.dart';

/// Servicio para gestionar vehículos del usuario
class VehiculoService {
  final ApiService apiService;

  VehiculoService({required this.apiService});

  /// Registrar un nuevo vehículo
  /// POST /api/v1/vehiculos/?usuario_id={id}
  Future<Map<String, dynamic>> registrarVehiculo({
    required int usuarioId,
    required String marca,
    required String modelo,
    required String placa,
    required String color,
    required int anio,
    String? vin,
    String? seguro,
  }) async {
    try {
      final response = await apiService.post(
        '/api/v1/vehiculos/',
        queryParams: {'usuario_id': usuarioId},
        body: {
          'marca': marca,
          'modelo': modelo,
          'placa': placa,
          'color': color,
          'anio': anio,
          'vin': vin,
          'seguro': seguro,
        },
      );

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al registrar vehículo: $e');
    }
  }

  /// Obtener todos los vehículos del usuario
  /// GET /api/v1/vehiculos/usuario/{propietario_id}
  Future<List<Map<String, dynamic>>> obtenerMisVehiculos({
    required int usuarioId,
  }) async {
    try {
      final response = await apiService.get(
        '/api/v1/vehiculos/usuario/$usuarioId',
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
      throw Exception('Error al obtener vehículos: $e');
    }
  }

  /// Obtener un vehículo específico
  /// GET /api/v1/vehiculos/{id}
  Future<Map<String, dynamic>> obtenerVehiculo({required int id}) async {
    try {
      final response = await apiService.get('/api/v1/vehiculos/$id');

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al obtener vehículo: $e');
    }
  }

  /// Actualizar datos del vehículo
  /// PUT /api/v1/vehiculos/{id}
  Future<Map<String, dynamic>> actualizarVehiculo({
    required int vehiculoId,
    required int usuarioId,
    String? color,
    String? seguro,
  }) async {
    try {
      final body = {
        if (color != null) 'color': color,
        if (seguro != null) 'seguro': seguro,
      };

      final response = await apiService.put(
        '/api/v1/vehiculos/$vehiculoId',
        body: body,
      );

      return response;
    } catch (e) {
      throw Exception('Error al actualizar vehículo: $e');
    }
  }

  /// Eliminar un vehículo
  /// DELETE /api/v1/vehiculos/{id}
  Future<Map<String, dynamic>> eliminarVehiculo({required int id}) async {
    try {
      final response = await apiService.delete('/api/v1/vehiculos/$id');

      return response;
    } catch (e) {
      throw Exception('Error al eliminar vehículo: $e');
    }
  }
}
