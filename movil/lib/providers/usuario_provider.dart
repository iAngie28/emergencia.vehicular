import 'package:flutter/material.dart';
import '../services/usuario_service.dart';

class UsuarioProvider extends ChangeNotifier {
  final UsuarioService usuarioService;

  Map<String, dynamic>? _perfil;
  bool _isLoading = false;
  String? _errorMessage;

  UsuarioProvider({required this.usuarioService});

  // Getters
  Map<String, dynamic>? get perfil => _perfil;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  /// Cargar perfil del usuario actual
  Future<void> cargarPerfil() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _perfil = await usuarioService.obtenerPerfil();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Actualizar perfil del usuario
  Future<bool> actualizarPerfil({
    String? nombre,
    String? apellido,
    String? telefono,
    String? direccion,
    String? ciudad,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final perfilActualizado = await usuarioService.actualizarPerfil(
        nombre: nombre,
        apellido: apellido,
        telefono: telefono,
        direccion: direccion,
        ciudad: ciudad,
      );

      _perfil = {...?_perfil, ...perfilActualizado};
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

  /// Cambiar contraseña
  Future<bool> cambiarContrasena({
    required String contrasenaActual,
    required String contrasenaNueva,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await usuarioService.cambiarContrasena(
        contrasenaActual: contrasenaActual,
        contrasenaNueva: contrasenaNueva,
      );

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

  /// Solicitar recuperación de contraseña
  Future<bool> solicitarRecuperacion({required String email}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await usuarioService.solicitarRecuperacionContrasena(email: email);
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
    _perfil = null;
    _errorMessage = null;
  }
}
