import 'package:flutter/foundation.dart';

class BackendConfig {
  static const String _defaultPort = '8000';

  // Override example:
  // flutter run --dart-define=BACKEND_URL=http://192.168.0.10:8000
  static String get baseUrl {
    const fromEnv = String.fromEnvironment('BACKEND_URL');
    if (fromEnv.isNotEmpty) return fromEnv;

    if (kIsWeb) return 'http://localhost:$_defaultPort';

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        // Android emulator: host machine is reachable via 10.0.2.2
        return 'http://10.0.2.2:$_defaultPort';
      case TargetPlatform.iOS:
        return 'http://localhost:$_defaultPort';
      default:
        return 'http://localhost:$_defaultPort';
    }
  }
}

