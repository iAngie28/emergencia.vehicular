import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'api_service.dart';

/// Servicio de autenticación - Conecta con el backend
class AuthService {
  final ApiService apiService;
  static const String _tokenKey = 'auth_token';
  static const String _userKey = 'user_data';

  AuthService({required this.apiService});

  /// Login - Conecta con /auth/login del backend
  /// Nota: El endpoint /auth/login usa OAuth2PasswordRequestForm que requiere form-encoded, no JSON
  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      // Hacer petición POST directamente con form-encoded
      final response = await http.post(
        Uri.parse('${apiService.baseUrl}/api/v1/auth/login'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
        },
        body: {
          'username': email,
          'password': password,
          'client_id': 'movil', // Indica que es desde la app móvil
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        // Guardar token localmente
        if (data != null && data['access_token'] != null) {
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString(_tokenKey, data['access_token']);
          if (data['user'] != null) {
            await prefs.setString(_userKey, data['user'].toString());
          }
        }

        return data;
      } else {
        final errorData = jsonDecode(response.body);
        throw Exception(
          errorData['detail'] ?? 'Error al iniciar sesión: ${response.statusCode}'
        );
      }
    } catch (e) {
      throw Exception('Error al iniciar sesión: $e');
    }
  }

  /// Obtiene el token guardado localmente
  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  /// Logout - Elimina el token local
  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_userKey);
  }

  /// Verifica si el usuario está autenticado
  Future<bool> isAuthenticated() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  /// Obtiene datos del usuario guardados localmente
  Future<String?> getUserData() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_userKey);
  }
}
