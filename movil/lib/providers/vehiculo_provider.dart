import 'package:flutter/material.dart';
import '../services/vehiculo_service.dart';

class VehiculoProvider extends ChangeNotifier {
  final VehiculoService vehiculoService;

  List<Map<String, dynamic>> _misVehiculos = [];
  Map<String, dynamic>? _vehiculoSeleccionado;
  bool _isLoading = false;
  String? _errorMessage;

  VehiculoProvider({required this.vehiculoService});

  // Getters
  List<Map<String, dynamic>> get misVehiculos => _misVehiculos;
  Map<String, dynamic>? get vehiculoSeleccionado => _vehiculoSeleccionado;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  /// Cargar mis vehículos
  Future<void> cargarMisVehiculos({required int usuarioId}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _misVehiculos = await vehiculoService.obtenerMisVehiculos(usuarioId: usuarioId);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Registrar un nuevo vehículo
  Future<bool> registrarVehiculo({
    required int usuarioId,
    required String marca,
    required String modelo,
    required String placa,
    required String color,
    required int anio,
    String? vin,
    String? seguro,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final nuevoVehiculo = await vehiculoService.registrarVehiculo(
        usuarioId: usuarioId,
        marca: marca,
        modelo: modelo,
        placa: placa,
        color: color,
        anio: anio,
        vin: vin,
        seguro: seguro,
      );

      _misVehiculos.add(nuevoVehiculo);
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

  /// Obtener detalles de un vehículo
  Future<void> obtenerVehiculo({required int id}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _vehiculoSeleccionado = await vehiculoService.obtenerVehiculo(id: id);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Actualizar un vehículo
  Future<bool> actualizarVehiculo({
    required int vehiculoId,
    required int usuarioId,
    String? color,
    String? seguro,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final vehiculoActualizado = await vehiculoService.actualizarVehiculo(
        vehiculoId: vehiculoId,
        usuarioId: usuarioId,
        color: color,
        seguro: seguro,
      );

      final index = _misVehiculos.indexWhere((v) => v['id'] == vehiculoId);
      if (index != -1) {
        _misVehiculos[index] = vehiculoActualizado;
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

  /// Eliminar un vehículo
  Future<bool> eliminarVehiculo({required int vehiculoId}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await vehiculoService.eliminarVehiculo(id: vehiculoId);
      _misVehiculos.removeWhere((v) => v['id'] == vehiculoId);
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

  void limpiar() {
    _misVehiculos = [];
    _vehiculoSeleccionado = null;
    _errorMessage = null;
  }
}
