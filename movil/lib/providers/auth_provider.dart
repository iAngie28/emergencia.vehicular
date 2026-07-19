import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/auth_service.dart';

/// Provider que maneja el estado de autenticación global
class AuthProvider extends ChangeNotifier {
  final AuthService authService;

  bool _isLoading = false;
  bool _isCheckingAuth = true;
  bool _isAuthenticated = false;
  String? _errorMessage;
  String? _userEmail;
  int? _userId;
  int? _roleId;
  String? _userName;
  bool _isTallerInhabilitado = false;

  AuthProvider({required this.authService}) {
    _checkAuthentication();
  }

  // Getters
  bool get isLoading => _isLoading;
  bool get isCheckingAuth => _isCheckingAuth;
  bool get isAuthenticated => _isAuthenticated;
  String? get errorMessage => _errorMessage;
  String? get userEmail => _userEmail;
  int? get userId => _userId;
  int? get roleId => _roleId;
  String? get userName => _userName;
  bool get isCliente => _roleId == AuthService.clienteRoleId;
  bool get isTecnico => _roleId == AuthService.tecnicoRoleId;
  String get roleLabel {
    if (isTecnico) return 'Tecnico';
    if (isCliente) return 'Cliente';
    return 'Usuario';
  }
  bool get isTallerInhabilitado => _isTallerInhabilitado;

  /// Verifica si hay sesión activa al iniciar
  Future<void> _checkAuthentication() async {
    _isAuthenticated = await authService.isAuthenticated();
    _userId = await authService.getCurrentUserId();
    _roleId = await authService.getCurrentUserRoleId();
    _userName = await authService.getCurrentUserName();
    _userEmail = await authService.getCurrentUserEmail();
    _isTallerInhabilitado = await authService.isTallerInhabilitado();
    _isCheckingAuth = false;
    notifyListeners();
  }

  /// Login - Conecta con el backend
  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final data = await authService.login(email: email, password: password);

      _isAuthenticated = true;
      _userEmail = email;
      _roleId = data['rol_id'] is int
          ? data['rol_id'] as int
          : int.tryParse('${data['rol_id']}');
      
      if (data['user'] is String) {
        _userName = data['user'];
      } else {
        _userName = data['nombre']?.toString();
      }

      _isTallerInhabilitado = data['taller_estado'] != null && data['taller_estado'] == false;

      final rawUserId = data['usuario_id'] ?? data['user_id'];
      if (rawUserId is int) {
        _userId = rawUserId;
      } else {
        _userId = await authService.getCurrentUserId();
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

  void setTallerInhabilitado(bool inhabilitado) {
    _isTallerInhabilitado = inhabilitado;
    notifyListeners();
    SharedPreferences.getInstance().then((prefs) {
      if (inhabilitado) {
        prefs.setBool('auth_taller_estado', false);
      } else {
        prefs.remove('auth_taller_estado');
      }
    });
  }

  /// Logout
  Future<void> logout() async {
    await authService.logout();
    _isAuthenticated = false;
    _userEmail = null;
    _userId = null;
    _roleId = null;
    _userName = null;
    _isTallerInhabilitado = false;
    _errorMessage = null;
    notifyListeners();
  }
}
