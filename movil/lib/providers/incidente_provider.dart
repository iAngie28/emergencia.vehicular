import 'package:flutter/material.dart';
import '../services/incidente_service.dart';

class IncidenteProvider extends ChangeNotifier {
  final IncidenteService incidenteService;

  List<Map<String, dynamic>> _misIncidentes = [];
  Map<String, dynamic>? _incidenteSeleccionado;
  bool _isLoading = false;
  String? _errorMessage;

  IncidenteProvider({required this.incidenteService});

  // Getters
  List<Map<String, dynamic>> get misIncidentes => _misIncidentes;
  Map<String, dynamic>? get incidenteSeleccionado => _incidenteSeleccionado;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  /// Cargar mis incidentes
  Future<void> cargarMisIncidentes({required int usuarioId}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _misIncidentes = await incidenteService.obtenerMisIncidentes(usuarioId: usuarioId);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Reportar un nuevo incidente
  Future<bool> reportarIncidente({
    required int usuarioId,
    required int vehiculoId,
    required String descripcion,
    required String ubicacion,
    required double latitud,
    required double longitud,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final nuevoIncidente = await incidenteService.reportarIncidente(
        usuarioId: usuarioId,
        vehiculoId: vehiculoId,
        descripcion: descripcion,
        ubicacion: ubicacion,
        latitud: latitud,
        longitud: longitud,
      );

      _misIncidentes.insert(0, nuevoIncidente);
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

  /// Obtener detalles de un incidente
  Future<void> obtenerIncidente({required int id}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _incidenteSeleccionado = await incidenteService.obtenerIncidente(id: id);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Actualizar estado del incidente
  Future<void> actualizarEstado({required int id}) async {
    try {
      final nuevoEstado = await incidenteService.obtenerEstadoIncidente(id: id);
      
      final index = _misIncidentes.indexWhere((inc) => inc['id'] == id);
      if (index != -1) {
        _misIncidentes[index] = {..._misIncidentes[index], ...nuevoEstado};
        notifyListeners();
      }
    } catch (e) {
      _errorMessage = e.toString();
      notifyListeners();
    }
  }

  void limpiar() {
    _misIncidentes = [];
    _incidenteSeleccionado = null;
    _errorMessage = null;
  }
}
