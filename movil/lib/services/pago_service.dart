import 'package:http/http.dart' as http;
import 'api_service.dart';

/// Servicio para gestionar pagos del usuario
class PagoService {
  final ApiService apiService;

  PagoService({required this.apiService});

  /// Obtener historial de pagos del usuario
  /// GET /api/v1/pagos/mi-historial?usuario_id={id}
  Future<List<Map<String, dynamic>>> obtenerMisHistorialPagos({
    required int usuarioId,
  }) async {
    try {
      final response = await apiService.get(
        '/api/v1/pagos/mi-historial',
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
      throw Exception('Error al obtener historial de pagos: $e');
    }
  }

  /// Obtener detalles de un pago específico
  /// GET /api/v1/pagos/{id}
  Future<Map<String, dynamic>> obtenerDetallePago({required int pagoId}) async {
    try {
      final response = await apiService.get('/api/v1/pagos/$pagoId');

      if (response is Map<String, dynamic>) {
        return response;
      } else {
        throw Exception('Respuesta inesperada del servidor');
      }
    } catch (e) {
      throw Exception('Error al obtener detalle de pago: $e');
    }
  }

  /// Registrar un pago realizado
  /// POST /api/v1/pagos/registrar
  Future<Map<String, dynamic>> registrarPago({
    required int incidenteId,
    required int usuarioId,
    required int tallerId,
    required double monto,
    required String metodoPago, // 'efectivo', 'tarjeta', 'transferencia'
    String? referencia,
  }) async {
    try {
      final response = await apiService.post(
        '/api/v1/pagos/registrar',
        body: {
          'incidente_id': incidenteId,
          'usuario_id': usuarioId,
          'taller_id': tallerId,
          'monto': monto,
          'metodo_pago': metodoPago,
          'referencia': referencia,
          'estado': 'completado',
        },
      );

      return response;
    } catch (e) {
      throw Exception('Error al registrar pago: $e');
    }
  }

  /// Obtener facturas pendientes (pagos por hacer)
  /// GET /api/v1/pagos/pendientes?usuario_id={id}
  Future<List<Map<String, dynamic>>> obtenerFacturasPendientes({
    required int usuarioId,
  }) async {
    try {
      final response = await apiService.get(
        '/api/v1/pagos/pendientes',
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
      throw Exception('Error al obtener facturas pendientes: $e');
    }
  }

  /// Descargar comprobante de pago (en PDF o imagen)
  /// GET /api/v1/pagos/{id}/comprobante
  Future<String> descargarComprobante({required int pagoId}) async {
    try {
      final response = await apiService.get('/api/v1/pagos/$pagoId/comprobante');

      if (response is Map<String, dynamic> && response['url'] != null) {
        return response['url'];
      } else {
        throw Exception('No se pudo descargar el comprobante');
      }
    } catch (e) {
      throw Exception('Error al descargar comprobante: $e');
    }
  }
}
