import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../backend_config.dart';
import '../models/emergencia_models.dart';

/// Service for handling emergency report submissions.
///
/// This service manages the complete workflow for submitting emergency reports
/// to the backend API, including:
/// - File validation (size and MIME type)
/// - Multipart HTTP requests
/// - Error handling and recovery
/// - Progress tracking
///
/// Usage:
/// ```dart
/// final service = EmergenciaService();
/// final result = await service.enviarReporte(
///   audioPath: '/path/to/audio.mp3',
///   imagePath: '/path/to/image.jpg',
///   onProgress: (progress) => print('Progress: ${(progress * 100).toStringAsFixed(1)}%'),
/// );
///
/// result.when(
///   success: (reporte) => print('Report submitted! Priority: ${reporte.priority}'),
///   failure: (error) => print('Error: ${error.message}'),
/// );
/// ```
class EmergenciaService {
  /// Base URL of the backend API (configured per platform)
  final String baseUrl;

  /// HTTP client instance for making requests
  final http.Client _client;

  /// Function to retrieve the JWT token for authentication
  final Future<String?> Function()? _getToken;

  /// Request timeout duration (default: 15 seconds)
  final Duration requestTimeout;

  /// Maximum allowed audio file size in bytes (25 MB)
  static const int maxAudioSizeBytes = 25 * 1024 * 1024;

  /// Maximum allowed image file size in bytes (10 MB)
  static const int maxImageSizeBytes = 10 * 1024 * 1024;

  /// Allowed audio MIME types
  static const List<String> allowedAudioMimes = [
    'audio/mpeg',
    'audio/wav',
    'audio/ogg',
    'audio/flac',
    'audio/mp4',
  ];

  /// Allowed image MIME types
  static const List<String> allowedImageMimes = [
    'image/jpeg',
    'image/png',
    'image/webp',
  ];

  /// Backend endpoint path for emergency reports
  static const String _emergenciaEndpoint = '/api/v1/emergencia/reportar';

  EmergenciaService({
    String? baseUrl,
    http.Client? client,
    Future<String?> Function()? getToken,
    Duration? requestTimeout,
  })  : baseUrl = baseUrl ?? BackendConfig.baseUrl,
        _client = client ?? http.Client(),
        _getToken = getToken,
        requestTimeout = requestTimeout ?? const Duration(seconds: 15);

  /// Determine MIME type based on file extension.
  ///
  /// Returns the MIME type string (e.g., 'audio/mpeg', 'image/jpeg') or null
  /// if the extension is not recognized.
  ///
  /// Example:
  /// ```dart
  /// String? mime = _getMimeType('audio.mp3');  // Returns 'audio/mpeg'
  /// String? mime = _getMimeType('photo.jpg');  // Returns 'image/jpeg'
  /// ```
  static String? _getMimeType(String filePath) {
    final ext = filePath.toLowerCase().split('.').last;

    // Audio MIME types
    const audioExtensions = {
      'mp3': 'audio/mpeg',
      'wav': 'audio/wav',
      'ogg': 'audio/ogg',
      'flac': 'audio/flac',
      'm4a': 'audio/mp4',
    };

    // Image MIME types
    const imageExtensions = {
      'jpg': 'image/jpeg',
      'jpeg': 'image/jpeg',
      'png': 'image/png',
      'webp': 'image/webp',
    };

    return audioExtensions[ext] ?? imageExtensions[ext];
  }

  /// Validate audio file.
  ///
  /// Checks:
  /// - File exists
  /// - File size does not exceed limit (25MB)
  /// - MIME type is allowed
  ///
  /// Throws [EmergenciaException] if validation fails.
  Future<void> _validateAudioFile(String filePath) async {
    final file = File(filePath);

    // Check if file exists
    if (!await file.exists()) {
      throw EmergenciaException(
        message: 'Audio file not found: $filePath',
      );
    }

    // Check file size
    final fileSize = await file.length();
    if (fileSize > maxAudioSizeBytes) {
      throw FileSizeException(
        fileName: file.path.split('/').last,
        fileSize: fileSize,
        maxSize: maxAudioSizeBytes,
      );
    }

    // Check MIME type
    final mimeType = _getMimeType(filePath);
    if (mimeType == null || !allowedAudioMimes.contains(mimeType)) {
      throw FileTypeException(
        fileName: file.path.split('/').last,
        fileType: mimeType ?? 'unknown',
        allowedTypes: allowedAudioMimes,
      );
    }
  }

  /// Validate image file.
  ///
  /// Checks:
  /// - File exists
  /// - File size does not exceed limit (10MB)
  /// - MIME type is allowed
  ///
  /// Throws [EmergenciaException] if validation fails.
  Future<void> _validateImageFile(String filePath) async {
    final file = File(filePath);

    // Check if file exists
    if (!await file.exists()) {
      throw EmergenciaException(
        message: 'Image file not found: $filePath',
      );
    }

    // Check file size
    final fileSize = await file.length();
    if (fileSize > maxImageSizeBytes) {
      throw FileSizeException(
        fileName: file.path.split('/').last,
        fileSize: fileSize,
        maxSize: maxImageSizeBytes,
      );
    }

    // Check MIME type
    final mimeType = _getMimeType(filePath);
    if (mimeType == null || !allowedImageMimes.contains(mimeType)) {
      throw FileTypeException(
        fileName: file.path.split('/').last,
        fileType: mimeType ?? 'unknown',
        allowedTypes: allowedImageMimes,
      );
    }
  }

  /// Get authentication headers for API requests.
  ///
  /// Returns a map of headers including:
  /// - Content-Type (if specified)
  /// - Authorization (JWT token if available)
  /// - Accept: application/json
  Future<Map<String, String>> _getHeaders({bool jsonContent = false}) async {
    // Retrieve JWT token from callback or SharedPreferences
    String? token = await _getToken?.call();
    token ??= (await SharedPreferences.getInstance()).getString('auth_token');

    return {
      if (jsonContent) 'Content-Type': 'application/json',
      'Accept': 'application/json',
      if (token != null && token.isNotEmpty) 'Authorization': 'Bearer $token',
    };
  }

  /// Parse the backend response into an [EmergenciaReporte].
  ///
  /// Handles both successful and partial responses.
  ///
  /// Returns [EmergenciaReporte] if parsing succeeds.
  /// Throws [EmergenciaException] if response format is invalid.
  EmergenciaReporte _parseResponse(String responseBody) {
    try {
      final json = jsonDecode(responseBody) as Map<String, dynamic>;
      return EmergenciaReporte.fromJson(json);
    } catch (e) {
      throw EmergenciaException(
        message: 'Failed to parse server response: $e',
        originalError: e,
      );
    }
  }

  /// Send emergency report to backend.
  ///
  /// Performs the following steps:
  /// 1. Validates both audio and image files
  /// 2. Creates a multipart HTTP request
  /// 3. Sends files to backend API
  /// 4. Handles various error scenarios
  /// 5. Parses and returns the backend response
  ///
  /// Parameters:
  /// - [audioPath]: Full path to audio file (e.g., '/path/to/audio.mp3')
  /// - [imagePath]: Full path to image file (e.g., '/path/to/image.jpg')
  /// - [onProgress]: Optional callback to track upload progress (0.0 - 1.0)
  ///
  /// Returns:
  /// - [Success]: Contains [EmergenciaReporte] with AI analysis results
  /// - [Failure]: Contains [EmergenciaException] describing the error
  ///
  /// Error Cases:
  /// - [FileSizeException]: If files exceed size limits
  /// - [FileTypeException]: If file MIME types are invalid
  /// - [NoInternetException]: If socket error occurs (no connectivity)
  /// - [TimeoutException]: If request exceeds 15 seconds
  /// - [HttpException]: If backend returns HTTP error
  ///
  /// Example:
  /// ```dart
  /// final result = await emergenciaService.enviarReporte(
  ///   audioPath: '/cache/emergency_audio.mp3',
  ///   imagePath: '/cache/scene_photo.jpg',
  ///   onProgress: (progress) {
  ///     print('Upload progress: ${(progress * 100).toStringAsFixed(0)}%');
  ///     // Update UI progress indicator
  ///   },
  /// );
  ///
  /// result.when(
  ///   success: (reporte) {
  ///     print('Status: ${reporte.processingStatus}');
  ///     print('Priority: ${reporte.priority}');
  ///     print('Transcription: ${reporte.transcription}');
  ///     for (var detection in reporte.detectionSummary) {
  ///       print('Detected: $detection');
  ///     }
  ///   },
  ///   failure: (error) {
  ///     print('Error: ${error.message}');
  ///     // Handle error appropriately
  ///   },
  /// );
  /// ```
  Future<Result<EmergenciaReporte>> enviarReporte({
    required String audioPath,
    required String imagePath,
    Function(double progress)? onProgress,
  }) async {
    try {
      // Step 1: Validate input files
      onProgress?.call(0.1);
      await _validateAudioFile(audioPath);
      await _validateImageFile(imagePath);

      // Step 2: Build multipart request
      onProgress?.call(0.2);
      final uri = Uri.parse('$baseUrl$_emergenciaEndpoint');
      final request = http.MultipartRequest('POST', uri);

      // Add headers (don't include Content-Type, http package sets it)
      final headers = await _getHeaders();
      request.headers.addAll(headers);

      // Step 3: Add audio file
      onProgress?.call(0.3);
      final audioFile = File(audioPath);
      final audioMime = _getMimeType(audioPath) ?? 'audio/mpeg';
      request.files.add(
        http.MultipartFile(
          'audio',
          audioFile.openRead(),
          await audioFile.length(),
          filename: audioFile.path.split('/').last,
          contentType: _parseMediaType(audioMime),
        ),
      );

      // Step 4: Add image file
      onProgress?.call(0.5);
      final imageFile = File(imagePath);
      final imageMime = _getMimeType(imagePath) ?? 'image/jpeg';
      request.files.add(
        http.MultipartFile(
          'imagen',
          imageFile.openRead(),
          await imageFile.length(),
          filename: imageFile.path.split('/').last,
          contentType: _parseMediaType(imageMime),
        ),
      );

      // Step 5: Send request with timeout
      onProgress?.call(0.7);
      final streamedResponse = await _client
          .send(request)
          .timeout(
            requestTimeout,
            onTimeout: () {
              throw TimeoutException(timeout: requestTimeout);
            },
          );

      onProgress?.call(0.9);

      // Step 6: Parse response
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        // Parse successful response
        final reporte = _parseResponse(response.body);
        onProgress?.call(1.0);
        return Success(reporte);
      } else if (response.statusCode == 413) {
        // Payload too large
        throw HttpException(
          statusCode: 413,
          message: 'File size exceeds server limits',
        );
      } else if (response.statusCode >= 500) {
        // Server error
        throw HttpException(
          statusCode: response.statusCode,
          message: 'Server error (${response.statusCode})',
          responseBody: response.body,
        );
      } else {
        // Other HTTP error
        throw HttpException(
          statusCode: response.statusCode,
          message: 'HTTP Error ${response.statusCode}',
          responseBody: response.body,
        );
      }
    } on EmergenciaException catch (e) {
      return Failure(e);
    } on SocketException catch (e) {
      // Network error (no internet or connection refused)
      if (e.message.contains('Connection refused') ||
          e.message.contains('Network is unreachable')) {
        return Failure(NoInternetException());
      }
      return Failure(
        EmergenciaException(
          message: 'Network error: ${e.message}',
          originalError: e,
        ),
      );
    } catch (e, stackTrace) {
      return Failure(
        EmergenciaException(
          message: 'Unexpected error: $e',
          originalError: e,
          stackTrace: stackTrace,
        ),
      );
    }
  }

  /// Parse a MIME type string into an http.MediaType.
  ///
  /// Example:
  /// ```dart
  /// var mediaType = _parseMediaType('audio/mpeg');
  /// // Returns MediaType('audio', 'mpeg')
  /// ```
  http.MediaType _parseMediaType(String mimeType) {
    final parts = mimeType.split('/');
    if (parts.length == 2) {
      return http.MediaType(parts[0], parts[1]);
    }
    return http.MediaType('application', 'octet-stream');
  }
}

