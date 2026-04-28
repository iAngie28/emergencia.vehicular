import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';

/// Provider que maneja el estado de autenticación global
class AuthProvider extends ChangeNotifier {
  final AuthService authService;

  bool _isLoading = false;
  bool _isAuthenticated = false;
  String? _errorMessage;
  String? _userEmail;
  int? _userId;

  AuthProvider({required this.authService}) {
    _checkAuthentication();
  }

  // Getters
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _isAuthenticated;
  String? get errorMessage => _errorMessage;
  String? get userEmail => _userEmail;
  int? get userId => _userId;

  /// Verifica si hay sesión activa al iniciar
  Future<void> _checkAuthentication() async {
    _isAuthenticated = await authService.isAuthenticated();
    _userId = await authService.getCurrentUserId();
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
      final rawUserId = data['user_id'];
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

  /// Logout
  Future<void> logout() async {
    await authService.logout();
    _isAuthenticated = false;
    _userEmail = null;
    _userId = null;
    _errorMessage = null;
    notifyListeners();
  }
}

/// Factory para crear el Provider
ChangeNotifierProvider<AuthProvider> authProvider() {
  return ChangeNotifierProvider<AuthProvider>(
    create: (context) => AuthProvider(
      authService: AuthService(
        apiService: ApiService(
          baseUrl: 'http://localhost:5000', // Cambia por tu URL del backend
          getToken: () async {
            // Este callback se ejecutará antes de cada petición
            final prefs = await context
                .read<AuthProvider>()
                .authService
                .getToken();
            return prefs;
          },
        ),
      ),
    ),
  );
}
