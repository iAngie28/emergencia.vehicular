import 'package:flutter/material.dart';
import '../services/pago_service.dart';

class PagoProvider extends ChangeNotifier {
  final PagoService pagoService;

  List<Map<String, dynamic>> _misPagos = [];
  List<Map<String, dynamic>> _facturasPendientes = [];
  Map<String, dynamic>? _pagoSeleccionado;
  bool _isLoading = false;
  String? _errorMessage;
  double _totalPendiente = 0.0;

  PagoProvider({required this.pagoService});

  // Getters
  List<Map<String, dynamic>> get misPagos => _misPagos;
  List<Map<String, dynamic>> get facturasPendientes => _facturasPendientes;
  Map<String, dynamic>? get pagoSeleccionado => _pagoSeleccionado;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  double get totalPendiente => _totalPendiente;

  /// Cargar historial de pagos
  Future<void> cargarHistorialPagos({required int usuarioId}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _misPagos = await pagoService.obtenerMisHistorialPagos(usuarioId: usuarioId);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Cargar facturas pendientes
  Future<void> cargarFacturasPendientes({required int usuarioId}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _facturasPendientes = await pagoService.obtenerFacturasPendientes(usuarioId: usuarioId);
      
      // Calcular total pendiente
      _totalPendiente = 0.0;
      for (var factura in _facturasPendientes) {
        if (factura['monto'] != null) {
          _totalPendiente += (factura['monto'] as num).toDouble();
        }
      }

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Obtener detalle de un pago
  Future<void> obtenerDetallePago({required int pagoId}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _pagoSeleccionado = await pagoService.obtenerDetallePago(pagoId: pagoId);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Registrar un pago realizado
  Future<bool> registrarPago({
    required int incidenteId,
    required int usuarioId,
    required int tallerId,
    required double monto,
    required String metodoPago,
    String? referencia,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final nuevoPago = await pagoService.registrarPago(
        incidenteId: incidenteId,
        usuarioId: usuarioId,
        tallerId: tallerId,
        monto: monto,
        metodoPago: metodoPago,
        referencia: referencia,
      );

      _misPagos.insert(0, nuevoPago);
      
      // Actualizar facturas pendientes
      _facturasPendientes.removeWhere((f) => f['incidente_id'] == incidenteId);
      
      // Recalcular total
      _totalPendiente = 0.0;
      for (var factura in _facturasPendientes) {
        if (factura['monto'] != null) {
          _totalPendiente += (factura['monto'] as num).toDouble();
        }
      }

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Descargar comprobante de pago
  Future<String?> descargarComprobante({required int pagoId}) async {
    try {
      return await pagoService.descargarComprobante(pagoId: pagoId);
    } catch (e) {
      _errorMessage = e.toString();
      notifyListeners();
      return null;
    }
  }

  void limpiar() {
    _misPagos = [];
    _facturasPendientes = [];
    _pagoSeleccionado = null;
    _totalPendiente = 0.0;
    _errorMessage = null;
  }
}
