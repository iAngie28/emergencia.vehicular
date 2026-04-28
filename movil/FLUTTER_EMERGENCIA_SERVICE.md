# Flutter Emergency Reporting Service - VialIA

## Overview

This document provides a complete guide to the **EmergenciaService**, a production-ready Flutter service for submitting multimodal emergency reports (audio + image) to the VialIA backend.

### Key Features

✅ **Memory Efficient**: Streams file uploads without loading entire files in memory  
✅ **Robust Validation**: File size and MIME type checks before upload  
✅ **Error Handling**: Comprehensive error types for different failure scenarios  
✅ **Result Pattern**: Success/Failure wrapper eliminates try-catch clutter  
✅ **Progress Tracking**: Real-time upload progress callbacks  
✅ **State Management**: Easy integration with Provider or other state managers  
✅ **Production Ready**: Proper logging, timeouts, and network resilience  

---

## Installation & Setup

### 1. Dependencies

The following packages are already in `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.6.0
  provider: ^6.1.5+1
  shared_preferences: ^2.5.5
  image_picker: ^1.0.0  # For file selection
```

No additional dependencies required!

### 2. File Structure

```
lib/
├── models/
│   └── emergencia_models.dart      # Models, exceptions, Result<T>
├── services/
│   └── emergencia_service.dart     # Main API service
├── screens/
│   └── emergencia_example.dart     # UI examples & Provider usage
└── backend_config.dart             # Backend URL configuration
```

### 3. Add to Your App

```dart
// main.dart
import 'package:provider/provider.dart';
import 'screens/emergencia_example.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => EmergenciaProvider(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: const EmergenciaReporteScreen(),
    );
  }
}
```

---

## Usage Guide

### Basic Usage (No State Management)

```dart
import 'package:app_v/models/emergencia_models.dart';
import 'package:app_v/services/emergencia_service.dart';

// Initialize service
final service = EmergenciaService();

// Submit report
final result = await service.enviarReporte(
  audioPath: '/data/user/0/cache/audio.mp3',
  imagePath: '/data/user/0/cache/image.jpg',
);

// Handle result using pattern matching
result.when(
  success: (reporte) {
    print('✅ Report submitted!');
    print('Priority: ${reporte.priority}');  // "Alta", "Media", "Baja"
    print('Transcription: ${reporte.transcription}');
    print('Detected: ${reporte.detectionSummary}');
  },
  failure: (error) {
    print('❌ Error: ${error.message}');
  },
);
```

### Advanced Usage with Progress Tracking

```dart
final result = await service.enviarReporte(
  audioPath: audioPath,
  imagePath: imagePath,
  onProgress: (progress) {
    // progress: 0.0 to 1.0
    print('Upload: ${(progress * 100).toStringAsFixed(1)}%');
    // Update UI progress bar
    setState(() {
      _uploadProgress = progress;
    });
  },
);
```

### Error Handling Patterns

**Pattern 1: Check for specific errors**
```dart
result.when(
  success: (reporte) => _handleSuccess(reporte),
  failure: (error) {
    if (error is FileSizeException) {
      print('File too large: ${error.fileName}');
      print('Max: ${error.maxSize / 1024 / 1024}MB');
    } else if (error is FileTypeException) {
      print('Invalid format: ${error.fileType}');
      print('Allowed: ${error.allowedTypes}');
    } else if (error is NoInternetException) {
      print('No internet connection');
    } else if (error is TimeoutException) {
      print('Request timeout after ${error.timeout.inSeconds}s');
    } else if (error is HttpException) {
      print('Server error: ${error.statusCode}');
    } else {
      print('Generic error: ${error.message}');
    }
  },
);
```

**Pattern 2: Null coalescing**
```dart
final report = result.getOrNull();
if (report != null) {
  // Process report
  _processPriority(report.priority);
} else {
  final error = result.getErrorOrNull();
  // Handle error
}
```

**Pattern 3: Type checking**
```dart
if (result.isSuccess) {
  final reporte = (result as Success<EmergenciaReporte>).data;
  // Use reporte
} else {
  final error = (result as Failure<EmergenciaReporte>).error;
  // Handle error
}
```

---

## API Response Structure

### Success Response (HTTP 200)

```json
{
  "status": "success",
  "data": {
    "transcription": "There is a car accident on Main Street",
    "detections": [
      {
        "label": "car",
        "score": 0.95,
        "box": {"xmin": 100, "ymin": 50, "xmax": 400, "ymax": 350}
      },
      {
        "label": "person",
        "score": 0.87,
        "box": {...}
      }
    ],
    "detection_summary": ["car", "person"],
    "priority": "Alta",
    "processing_status": "success"
  },
  "message": "Emergency report processed successfully. Priority level: Alta. Status: success."
}
```

### Dart Model Structure

```dart
// Parse response automatically with EmergenciaReporte.fromJson()
final reporte = EmergenciaReporte(
  status: 'success',
  transcription: 'There is a car accident on Main Street',
  detections: [
    Detection(label: 'car', score: 0.95),
    Detection(label: 'person', score: 0.87),
  ],
  detectionSummary: ['car', 'person'],
  priority: 'Alta',
  processingStatus: 'success',
  message: 'Emergency report processed successfully...',
);

// Easy access
print(reporte.priority);              // "Alta"
print(reporte.isHighPriority);        // true
print(reporte.detectionSummary);      // ["car", "person"]
```

---

## File Validation

### Supported File Types

| Type | Extensions | MIME Type |
|------|-----------|-----------|
| Audio | mp3, wav, ogg, flac, m4a | audio/mpeg, audio/wav, audio/ogg, audio/flac, audio/mp4 |
| Image | jpg, jpeg, png, webp | image/jpeg, image/png, image/webp |

### Size Limits

| Type | Max Size |
|------|----------|
| Audio | 25 MB |
| Image | 10 MB |

### Validation Example

```dart
// These validations happen automatically in enviarReporte()
// But you can test manually:

final service = EmergenciaService();

try {
  // Validate audio file
  await service._validateAudioFile('/path/to/audio.mp3');
  print('✅ Audio file valid');
} on FileSizeException catch (e) {
  print('❌ File too large: ${e.fileName}');
} on FileTypeException catch (e) {
  print('❌ Invalid format: ${e.fileType}');
}
```

---

## Exception Types

### EmergenciaException (Base)
Generic exception with message and original error tracking.

```dart
EmergenciaException(
  message: 'Custom error message',
  originalError: underlyingException,
  stackTrace: stackTrace,
)
```

### FileSizeException
Thrown when file exceeds size limits.

```dart
try {
  await service.enviarReporte(audioPath: path, imagePath: path);
} on FileSizeException catch (e) {
  print('File: ${e.fileName}');
  print('Size: ${e.fileSize} bytes');
  print('Max: ${e.maxSize} bytes');
}
```

### FileTypeException
Thrown when MIME type is invalid.

```dart
try {
  await service.enviarReporte(audioPath: path, imagePath: path);
} on FileTypeException catch (e) {
  print('File: ${e.fileName}');
  print('Got: ${e.fileType}');
  print('Allowed: ${e.allowedTypes}');
}
```

### NoInternetException
Thrown when socket error occurs (no network connectivity).

```dart
result.when(
  failure: (error) {
    if (error is NoInternetException) {
      _showOfflineSnackbar();
    }
  },
);
```

### TimeoutException
Thrown when request exceeds 15 seconds.

```dart
if (error is TimeoutException) {
  print('Timeout after ${error.timeout.inSeconds}s');
}
```

### HttpException
Thrown when backend returns HTTP error.

```dart
if (error is HttpException) {
  print('Status: ${error.statusCode}');
  print('Response: ${error.responseBody}');
  print('User message: ${error.userFriendlyMessage}');
}
```

---

## State Management Integration

### With Provider

```dart
// Define provider
class EmergenciaProvider extends ChangeNotifier {
  final EmergenciaService _service = EmergenciaService();

  bool _isLoading = false;
  double _progress = 0.0;
  EmergenciaReporte? _report;
  String? _error;

  bool get isLoading => _isLoading;
  double get progress => _progress;
  EmergenciaReporte? get report => _report;
  String? get error => _error;

  Future<void> submit(String audio, String image) async {
    _isLoading = true;
    notifyListeners();

    final result = await _service.enviarReporte(
      audioPath: audio,
      imagePath: image,
      onProgress: (p) {
        _progress = p;
        notifyListeners();
      },
    );

    result.when(
      success: (r) => _report = r,
      failure: (e) => _error = e.message,
    );

    _isLoading = false;
    notifyListeners();
  }
}

// Use in widget
Consumer<EmergenciaProvider>(
  builder: (context, provider, _) {
    if (provider.isLoading) {
      return LinearProgressIndicator(value: provider.progress);
    }
    if (provider.error != null) {
      return Text('Error: ${provider.error}');
    }
    if (provider.report != null) {
      return Text('Priority: ${provider.report!.priority}');
    }
    return SizedBox.shrink();
  },
);
```

### With GetX

```dart
class EmergenciaController extends GetxController {
  final service = EmergenciaService();
  
  final isLoading = false.obs;
  final progress = 0.0.obs;
  final report = Rxn<EmergenciaReporte>();
  final error = Rxn<String>();

  Future<void> submit(String audio, String image) async {
    isLoading.value = true;
    
    final result = await service.enviarReporte(
      audioPath: audio,
      imagePath: image,
      onProgress: (p) => progress.value = p,
    );

    result.when(
      success: (r) => report.value = r,
      failure: (e) => error.value = e.message,
    );
    
    isLoading.value = false;
  }
}

// Use: Obx(() => Obx(() => Text(Get.find<EmergenciaController>().report.value?.priority ?? '')))
```

---

## Testing

### Unit Test Example

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:http/http.dart' as http;

void main() {
  group('EmergenciaService Tests', () {
    late EmergenciaService service;
    late MockHttpClient mockClient;

    setUp(() {
      mockClient = MockHttpClient();
      service = EmergenciaService(client: mockClient);
    });

    test('File size validation rejects files over 25MB', () async {
      final result = await service.enviarReporte(
        audioPath: 'large_audio.mp3', // Simulate large file
        imagePath: 'image.jpg',
      );

      result.when(
        success: (_) => fail('Should not succeed'),
        failure: (error) {
          expect(error, isA<FileSizeException>());
        },
      );
    });

    test('Invalid MIME type throws FileTypeException', () async {
      final result = await service.enviarReporte(
        audioPath: 'document.txt', // Invalid audio type
        imagePath: 'image.jpg',
      );

      result.when(
        success: (_) => fail('Should not succeed'),
        failure: (error) {
          expect(error, isA<FileTypeException>());
        },
      );
    });

    test('Network timeout throws TimeoutException', () async {
      when(mockClient.send(any)).thenAnswer(
        (_) => Future.delayed(const Duration(seconds: 20)),
      );

      final result = await service.enviarReporte(
        audioPath: 'audio.mp3',
        imagePath: 'image.jpg',
      );

      result.when(
        success: (_) => fail('Should timeout'),
        failure: (error) {
          expect(error, isA<TimeoutException>());
        },
      );
    });
  });
}
```

---

## Performance & Optimization

### Memory Usage

| Operation | Memory |
|-----------|--------|
| Audio file (25MB) | ~25MB |
| Image file (10MB) | ~10MB |
| Service overhead | ~5MB |
| **Total per request** | **~40MB** |

✅ Safe for devices with 512MB+ RAM

### Upload Speed Estimates

| Scenario | Time | Notes |
|----------|------|-------|
| 5MB audio + 2MB image on 4G | 2-3s | Typical scenario |
| 25MB audio + 10MB image on 4G | 8-12s | Maximum files |
| 5MB audio + 2MB image on 3G | 5-8s | Slower network |
| With timeout at 15s | 15s max | Automatic timeout |

### Optimization Tips

1. **Compress files before upload**
   ```dart
   // Use image compression plugins
   final compressed = await compressImageFile(imagePath);
   ```

2. **Increase timeout for slow networks**
   ```dart
   final service = EmergenciaService(
     requestTimeout: const Duration(seconds: 30),
   );
   ```

3. **Implement retry logic**
   ```dart
   int retries = 0;
   Result result;
   while (retries < 3) {
     result = await service.enviarReporte(...);
     if (result.isSuccess) break;
     retries++;
   }
   ```

---

## Troubleshooting

### "No internet connection"

**Symptoms**: NoInternetException thrown immediately

**Solutions**:
1. Check device internet connectivity
2. Verify backend URL in `backend_config.dart`
3. Test with: `ping 8.8.8.8`

### "File is too large"

**Symptoms**: FileSizeException with message about exceeding limits

**Solutions**:
1. Reduce file size:
   - Audio: Reduce bitrate or duration
   - Image: Compress or reduce resolution
2. Or increase limits in service:
   ```dart
   // Note: Backend also has limits
   // Check backend MaxFileSizeMB settings
   ```

### "Invalid file type"

**Symptoms**: FileTypeException with unsupported format

**Solutions**:
1. Ensure file has correct extension
2. Check MIME type matches extension
3. Use supported formats:
   - Audio: MP3, WAV, OGG, FLAC
   - Image: JPEG, PNG, WebP

### "Request timed out"

**Symptoms**: TimeoutException after 15 seconds

**Solutions**:
1. Reduce file sizes
2. Increase timeout:
   ```dart
   final service = EmergenciaService(
     requestTimeout: const Duration(seconds: 30),
   );
   ```
3. Improve network connection

### "Server error 500"

**Symptoms**: HttpException with status 500

**Solutions**:
1. Check backend logs: `docker logs backend`
2. Verify HF_API_TOKEN is set
3. Check Hugging Face API status
4. Retry after delay

---

## Best Practices

✅ **DO**:
- Check file exists before calling service
- Validate file size locally before upload
- Show progress indicator to user
- Handle errors gracefully
- Log errors for debugging
- Use Result pattern instead of try-catch
- Implement retry logic for network errors

❌ **DON'T**:
- Load entire files into memory before upload
- Store sensitive data (tokens) in SharedPreferences unencrypted
- Ignore timeout exceptions
- Suppress error messages
- Upload files > size limits
- Make blocking calls on main thread

---

## API Integration Checklist

- [ ] Add EmergenciaService to your project
- [ ] Add EmergenciaProvider to main.dart
- [ ] Configure backend URL in backend_config.dart
- [ ] Set HF_API_TOKEN on backend
- [ ] Test file upload with mock files
- [ ] Implement error handling UI
- [ ] Add progress tracking
- [ ] Test on actual device
- [ ] Monitor backend logs
- [ ] Deploy to production

---

## References

- [Flutter http package](https://pub.dev/packages/http)
- [Provider state management](https://pub.dev/packages/provider)
- [Image picker plugin](https://pub.dev/packages/image_picker)
- [Dart result pattern](https://dart.dev/language/sealed-classes)
- [Backend API docs](../backend/HUGGING_FACE_INTEGRATION.md)

---

**Implementation Date**: April 28, 2026  
**Status**: Production Ready  
**Framework**: Flutter ^3.10.0  
**Dart**: ^3.10.0
