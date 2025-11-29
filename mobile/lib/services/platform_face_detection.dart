import 'dart:typed_data';

import 'package:flutter/foundation.dart';

import 'face_detection_service.dart';

// Conditional import for web platform
// ignore: uri_does_not_exist
import 'face_detection_web.dart' if (dart.library.io) 'face_detection_stub.dart';

/// Platform-aware face detection service
/// Automatically uses the appropriate implementation based on platform:
/// - Web: Uses face-api.js via JavaScript interop
/// - Mobile: Uses Google ML Kit (native)
class PlatformFaceDetection {
  static final PlatformFaceDetection _instance = PlatformFaceDetection._internal();
  factory PlatformFaceDetection() => _instance;
  PlatformFaceDetection._internal();

  // Native service for mobile platforms
  final FaceDetectionService _nativeService = FaceDetectionService();
  
  // Web service - will be null on non-web platforms
  dynamic _webService;
  
  bool _isInitialized = false;

  /// Check if we're running on web
  bool get isWeb => kIsWeb;

  /// Initialize the appropriate face detection service
  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      if (kIsWeb) {
        debugPrint('PlatformFaceDetection: Using web face-api.js');
        _webService = FaceDetectionWebService();
        await (_webService as FaceDetectionWebService).initialize();
      } else {
        debugPrint('PlatformFaceDetection: Using native ML Kit');
        await _nativeService.initialize();
      }
      _isInitialized = true;
    } catch (e) {
      debugPrint('PlatformFaceDetection initialization error: $e');
      rethrow;
    }
  }

  /// Detect faces in an image
  Future<FaceDetectionResult> detectFaces(Uint8List imageBytes) async {
    if (!_isInitialized) {
      await initialize();
    }

    if (kIsWeb) {
      return await (_webService as FaceDetectionWebService).detectFaces(imageBytes);
    } else {
      return await _nativeService.detectFaces(imageBytes);
    }
  }

  /// Validate face image for skin analysis
  Future<FaceValidationResult> validateFaceImage(Uint8List imageBytes) async {
    if (!_isInitialized) {
      await initialize();
    }

    if (kIsWeb) {
      return await (_webService as FaceDetectionWebService).validateFaceImage(imageBytes);
    } else {
      return await _nativeService.validateFaceImage(imageBytes);
    }
  }

  /// Get skin analysis zones from detected face
  Map<String, FaceRect> getSkinAnalysisZones(DetectedFace face) {
    if (kIsWeb) {
      return (_webService as FaceDetectionWebService).getSkinAnalysisZones(face);
    } else {
      return _nativeService.getSkinAnalysisZones(face);
    }
  }

  void dispose() {
    if (kIsWeb && _webService != null) {
      (_webService as FaceDetectionWebService).dispose();
    } else {
      _nativeService.dispose();
    }
    _isInitialized = false;
  }
}
