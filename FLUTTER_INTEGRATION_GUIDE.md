# Flutter Mobile App - Production Integration Guide

## Overview

This guide explains how to configure your Flutter app to connect to the VialIA backend in both development and production environments.

---

## 1. Current Flutter Configuration

### **File: `lib/backend_config.dart`**

Your existing config is excellent! It handles:

```dart
✅ Android Emulator: http://10.0.2.2:8000
✅ iOS Simulator: http://localhost:8000
✅ Physical Device: http://192.168.56.1:8000
✅ Environment Variable Override: BACKEND_URL
✅ Production Build Mode: -DPRODUCTION_BUILD=true
```

---

## 2. Production Deployment Scenarios

### **Scenario A: Production Render Backend**

**After Render deployment**:

```bash
# Render auto-provides:
# Service URL: https://vialia-backend.onrender.com

# Android Release Build
flutter build apk --release \
  --dart-define=PRODUCTION_BUILD=true

# iOS Release Build
flutter build ios --release \
  --dart-define=PRODUCTION_BUILD=true

# Result: App uses https://vialia-backend.onrender.com
```

### **Scenario B: Custom Domain**

**If you have your own domain**:

```bash
# Build with custom backend URL
flutter build apk --release \
  --dart-define=BACKEND_URL=https://api.yourdomain.com

# iOS
flutter build ios --release \
  --dart-define=BACKEND_URL=https://api.yourdomain.com
```

### **Scenario C: Local Development with Physical Device**

**Your physical device and computer on same network**:

```bash
# Build for local network
flutter run --dart-define=BACKEND_URL=http://192.168.56.1:8000

# or
flutter run  # Auto-selects based on platform
```

---

## 3. Update Backend Configuration in Flutter

### **Recommended: Enhanced `lib/backend_config.dart`**

```dart
import 'package:flutter/foundation.dart';

/// VialIA Backend Configuration
/// Manages dynamic backend URL based on platform, device, and environment
class BackendConfig {
  // ===== DEFAULT PORTS =====
  static const String _defaultPort = '8000';
  
  // ===== LOCAL NETWORK CONFIGURATION =====
  static const String _localNetworkIp = '192.168.56.1';  // Your machine's IP
  static const String _androidEmulatorHost = '10.0.2.2';  // Android emulator special IP
  
  // ===== PRODUCTION URLS =====
  // Update these after Render deployment
  static const String _productionBackendUrl = 'https://vialia-backend.onrender.com';
  static const String _productionFrontendUrl = 'https://vialia-frontend.onrender.com';
  
  // ===== DEVELOPMENT URLS =====
  static const String _localDevUrl = 'http://localhost:$_defaultPort';
  static const String _localNetworkUrl = 'http://$_localNetworkIp:$_defaultPort';
  static const String _androidEmulatorUrl = 'http://$_androidEmulatorHost:$_defaultPort';

  /// Main backend API URL
  /// Priority:
  /// 1. Environment variable (BACKEND_URL)
  /// 2. Production build flag
  /// 3. Platform-specific defaults
  static String get baseUrl {
    // === 1. Check Environment Variable ===
    const fromEnv = String.fromEnvironment('BACKEND_URL');
    if (fromEnv.isNotEmpty) {
      debugPrint('[CONFIG] Backend URL from env: $fromEnv');
      return fromEnv;
    }

    // === 2. Check Production Build ===
    if (const bool.fromEnvironment('PRODUCTION_BUILD') == true) {
      debugPrint('[CONFIG] Production build - using: $_productionBackendUrl');
      return _productionBackendUrl;
    }

    // === 3. Platform-Specific Development URLs ===
    if (kIsWeb) {
      debugPrint('[CONFIG] Web platform - using: $_localDevUrl');
      return _localDevUrl;
    }

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        // Check if emulator or physical device
        String url = _isEmulator() ? _androidEmulatorUrl : _localNetworkUrl;
        debugPrint('[CONFIG] Android - using: $url');
        return url;
        
      case TargetPlatform.iOS:
        // iOS simulator uses localhost, physical device uses local network
        String url = _isSimulator() ? _localDevUrl : _localNetworkUrl;
        debugPrint('[CONFIG] iOS - using: $url');
        return url;
        
      default:
        debugPrint('[CONFIG] Default - using: $_localDevUrl');
        return _localDevUrl;
    }
  }

  /// Android Emulator Detection
  /// Returns true if running on Android emulator
  static bool _isEmulator() {
    // TODO: Implement emulator detection
    // For now, assumes physical device on local network
    return false;
  }

  /// iOS Simulator Detection
  /// Returns true if running on iOS simulator
  static bool _isSimulator() {
    // TODO: Implement simulator detection
    // For now, assumes physical device on local network
    return false;
  }

  // ===== CONVENIENCE URLS =====
  
  /// Frontend URL (for linking to web app if needed)
  static String get frontendUrl => _productionFrontendUrl;
  
  /// Emulator URL (for testing)
  static String get androidEmulatorUrl => _androidEmulatorUrl;
  
  /// Physical device URL (for testing)
  static String get physicalDeviceUrl => _localNetworkUrl;
  
  /// Local development URL
  static String get localDevUrl => _localDevUrl;

  // ===== DEBUGGING & INFO =====
  
  /// Print debug information about current configuration
  static void printDebugInfo() {
    debugPrint('');
    debugPrint('╔════════════════════════════════════════════╗');
    debugPrint('║         VialIA Backend Configuration       ║');
    debugPrint('╠════════════════════════════════════════════╣');
    debugPrint('║ Current Backend URL: $baseUrl');
    debugPrint('║ Environment: ${const bool.fromEnvironment('PRODUCTION_BUILD') ? 'PRODUCTION' : 'DEVELOPMENT'}');
    debugPrint('║ Platform: ${defaultTargetPlatform.toString().split('.').last}');
    debugPrint('║ Is Web: $kIsWeb');
    debugPrint('╠════════════════════════════════════════════╣');
    debugPrint('║ Available URLs:');
    debugPrint('║  - Production: $_productionBackendUrl');
    debugPrint('║  - Local Dev: $_localDevUrl');
    debugPrint('║  - Local Network: $_localNetworkUrl');
    debugPrint('║  - Emulator: $_androidEmulatorUrl');
    debugPrint('╚════════════════════════════════════════════╝');
    debugPrint('');
  }

  /// Get full API endpoint URL
  static String apiUrl(String endpoint) {
    return '$baseUrl/api/v1/$endpoint';
  }

  /// Get specific service endpoints
  static String get emergenciaEndpoint => apiUrl('emergencia');
  static String get authEndpoint => apiUrl('auth');
  static String get usuariosEndpoint => apiUrl('usuarios');
  static String get incidentesEndpoint => apiUrl('incidentes');
  static String get vehiculosEndpoint => apiUrl('vehiculos');
}
```

---

## 4. HTTP Client Configuration

### **Create: `lib/services/http_client.dart`**

```dart
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';
import 'package:vialia/config/backend_config.dart';

class VialiaHttpClient {
  static final VialiaHttpClient _instance = VialiaHttpClient._internal();

  factory VialiaHttpClient() {
    return _instance;
  }

  VialiaHttpClient._internal();

  /// Create HTTP headers with common configuration
  static Map<String, String> get commonHeaders {
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'User-Agent': 'VialIA-Mobile/1.0',
    };
  }

  /// Make GET request
  static Future<http.Response> get(String endpoint) async {
    try {
      final url = Uri.parse('${BackendConfig.baseUrl}$endpoint');
      debugPrint('[HTTP] GET $url');
      
      final response = await http.get(url, headers: commonHeaders).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );
      
      _logResponse(response);
      return response;
    } catch (e) {
      debugPrint('[HTTP] GET Error: $e');
      rethrow;
    }
  }

  /// Make POST request with JSON body
  static Future<http.Response> post(
    String endpoint, {
    required Map<String, dynamic> body,
  }) async {
    try {
      final url = Uri.parse('${BackendConfig.baseUrl}$endpoint');
      debugPrint('[HTTP] POST $url');
      debugPrint('[HTTP] Body: $body');
      
      final response = await http.post(
        url,
        headers: commonHeaders,
        body: jsonEncode(body),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );
      
      _logResponse(response);
      return response;
    } catch (e) {
      debugPrint('[HTTP] POST Error: $e');
      rethrow;
    }
  }

  /// Make multipart request (for file uploads)
  static Future<http.StreamedResponse> postMultipart(
    String endpoint, {
    required Map<String, String> fields,
    required Map<String, String> files, // filename -> filepath
  }) async {
    try {
      final url = Uri.parse('${BackendConfig.baseUrl}$endpoint');
      debugPrint('[HTTP] POST (multipart) $url');
      
      var request = http.MultipartRequest('POST', url);
      request.headers.addAll(commonHeaders);
      
      // Add fields
      fields.forEach((key, value) {
        request.fields[key] = value;
        debugPrint('[HTTP] Field: $key = $value');
      });
      
      // Add files
      for (var entry in files.entries) {
        final file = File(entry.value);
        request.files.add(
          await http.MultipartFile.fromPath(entry.key, entry.value),
        );
        debugPrint('[HTTP] File: ${entry.key} = ${entry.value}');
      }
      
      final streamedResponse = await request.send().timeout(
        const Duration(seconds: 120), // Longer timeout for file upload
        onTimeout: () => throw Exception('Upload timeout'),
      );
      
      debugPrint('[HTTP] Response: ${streamedResponse.statusCode}');
      return streamedResponse;
    } catch (e) {
      debugPrint('[HTTP] Multipart Error: $e');
      rethrow;
    }
  }

  /// Log response for debugging
  static void _logResponse(http.Response response) {
    debugPrint('[HTTP] Status: ${response.statusCode}');
    if (response.statusCode < 300) {
      debugPrint('[HTTP] Response (truncated): ${response.body.substring(0, math.min(200, response.body.length))}...');
    } else {
      debugPrint('[HTTP] Error Response: ${response.body}');
    }
  }
}
```

---

## 5. Emergency Report Service

### **Create: `lib/services/emergency_service.dart`**

```dart
import 'package:http/http.dart' as http;
import 'package:vialia/config/backend_config.dart';
import 'package:vialia/services/http_client.dart';

class EmergencyService {
  /// Report emergency with audio and image
  static Future<Map<String, dynamic>> reportEmergency({
    required String audioFilePath,
    required String imageFilePath,
  }) async {
    try {
      debugPrint('[EMERGENCY] Reporting emergency...');
      debugPrint('[EMERGENCY] Audio: $audioFilePath');
      debugPrint('[EMERGENCY] Image: $imageFilePath');
      
      final response = await VialiaHttpClient.postMultipart(
        '/api/v1/emergencia/reportar',
        fields: {}, // No additional fields needed
        files: {
          'audio': audioFilePath,
          'imagen': imageFilePath,
        },
      );
      
      final responseBody = await response.stream.bytesToString();
      debugPrint('[EMERGENCY] Response: $responseBody');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(responseBody);
        return {
          'success': true,
          'data': data,
        };
      } else {
        return {
          'success': false,
          'error': 'Server error: ${response.statusCode}',
          'response': responseBody,
        };
      }
    } catch (e) {
      debugPrint('[EMERGENCY] Error: $e');
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }
}
```

---

## 6. Build Commands for Different Environments

### **Local Development**

```bash
# Android Emulator
flutter run

# iOS Simulator
flutter run -d all  # or specific simulator

# Physical Device
flutter run
```

### **Development - Custom Local URL**

```bash
# If backend is not at default http://192.168.56.1:8000
flutter run --dart-define=BACKEND_URL=http://192.168.1.100:8000
```

### **Production - Render Backend**

```bash
# Android APK
flutter build apk --release \
  --dart-define=PRODUCTION_BUILD=true \
  --build-number=1.0.0 \
  --build-name=1.0.0

# Android App Bundle (for Play Store)
flutter build appbundle --release \
  --dart-define=PRODUCTION_BUILD=true \
  --build-number=1.0.0 \
  --build-name=1.0.0

# iOS
flutter build ios --release \
  --dart-define=PRODUCTION_BUILD=true \
  --build-number=1.0.0 \
  --build-name=1.0.0
```

### **Production - Custom Domain**

```bash
# Android
flutter build apk --release \
  --dart-define=BACKEND_URL=https://api.yourdomain.com \
  --build-number=1.0.0

# iOS
flutter build ios --release \
  --dart-define=BACKEND_URL=https://api.yourdomain.com \
  --build-number=1.0.0
```

---

## 7. Testing Connectivity

### **In Flutter App**

```dart
void main() {
  // Print configuration on startup
  BackendConfig.printDebugInfo();
  
  // Test connectivity
  testBackendConnection();
  
  runApp(const MyApp());
}

Future<void> testBackendConnection() async {
  try {
    final response = await http.get(
      Uri.parse('${BackendConfig.baseUrl}/health'),
    ).timeout(const Duration(seconds: 5));
    
    if (response.statusCode == 200) {
      debugPrint('✓ Backend connection: OK');
      debugPrint('✓ Backend URL: ${BackendConfig.baseUrl}');
    } else {
      debugPrint('✗ Backend returned status: ${response.statusCode}');
    }
  } catch (e) {
    debugPrint('✗ Backend connection failed: $e');
    debugPrint('  Trying: ${BackendConfig.baseUrl}/health');
  }
}
```

### **Via curl from Terminal**

```bash
# Test backend health
curl -i http://10.0.2.2:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "vialia-backend",
#   "ai_enabled": true
# }

# Test readiness
curl -i http://10.0.2.2:8000/ready

# Test AI endpoint (local development)
curl -X POST http://10.0.2.2:8000/api/v1/emergencia/reportar \
  -F "audio=@emergency.mp3" \
  -F "imagen=@scene.jpg"
```

---

## 8. Common Issues & Solutions

### **Issue: Connection Refused**

**Problem**: `Connection refused` error when trying to reach backend

**Solutions**:
1. ✅ Verify backend is running: `python main.py` in backend directory
2. ✅ Check URL: iOS uses `localhost`, Android uses `10.0.2.2`
3. ✅ Firewall: Ensure port 8000 is accessible
4. ✅ Same network: Device and machine must be on same WiFi network

### **Issue: CORS Error**

**Problem**: `No 'Access-Control-Allow-Origin' header`

**Solutions**:
1. ✅ Check backend URL is correctly set in `BackendConfig`
2. ✅ Verify `RENDER_EXTERNAL_URL` is set on Render
3. ✅ Restart backend: Changes to main.py require restart
4. ✅ Clear app cache: `flutter clean && flutter pub get`

### **Issue: Timeout**

**Problem**: Request times out or is very slow

**Solutions**:
1. ✅ Check network connectivity
2. ✅ Increase timeout in HTTP client (default 30s)
3. ✅ For AI endpoint: First request may be slow as models load
4. ✅ Check Render logs for backend issues

### **Issue: AI Features Not Working**

**Problem**: Emergency endpoint returns 500 error

**Solutions**:
1. ✅ Check `HF_API_TOKEN` is set on Render
2. ✅ Verify Hugging Face account has sufficient credits
3. ✅ Check Hugging Face API status: https://status.huggingface.co
4. ✅ Test with valid audio/image files

---

## 9. Environment-Specific Configuration Summary

| Scenario | Build Command | Backend URL | Notes |
|----------|---------------|-------------|-------|
| **Android Emulator** | `flutter run` | `http://10.0.2.2:8000` | Auto-selected |
| **iOS Simulator** | `flutter run` | `http://localhost:8000` | Auto-selected |
| **Physical Device** | `flutter run` | `http://192.168.56.1:8000` | Same WiFi network |
| **Custom Network** | `flutter run --dart-define=BACKEND_URL=...` | Custom | Your choice |
| **Production Render** | `flutter build --dart-define=PRODUCTION_BUILD=true` | `https://vialia-backend.onrender.com` | From env |
| **Production Custom** | `flutter build --dart-define=BACKEND_URL=...` | Your domain | Your choice |

---

## 10. Checklist Before Release

- [ ] `BackendConfig.baseUrl` returns correct URL for all platforms
- [ ] Emergency endpoint accepts files and returns priority assessment
- [ ] CORS configuration allows Flutter app origin
- [ ] Audio and image file formats are supported
- [ ] File size limits are appropriate (25MB audio, 10MB image)
- [ ] Error messages are user-friendly (not showing stack traces)
- [ ] Timeout values are reasonable (30s for upload, 120s for AI processing)
- [ ] Health check endpoint returns expected response
- [ ] App handles network errors gracefully
- [ ] Logging is informative but not verbose in production

---

## Support & Resources

- **Backend Config**: `lib/backend_config.dart`
- **HTTP Client**: `lib/services/http_client.dart`
- **Emergency Service**: `lib/services/emergency_service.dart`
- **Server Logs**: Check Render dashboard → Logs
- **API Documentation**: Check `PRODUCTION_DEPLOYMENT_GUIDE.md`

Good luck with your Flutter app! 🚀
