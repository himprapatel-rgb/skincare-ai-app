import 'dart:typed_data';

import 'face_detection_service.dart';

/// Stub implementation of FaceDetectionWebService for non-web platforms
/// This file is used for conditional imports - it will never actually run
/// because kIsWeb will be false on non-web platforms
class FaceDetectionWebService {
  static final FaceDetectionWebService _instance = FaceDetectionWebService._internal();
  factory FaceDetectionWebService() => _instance;
  FaceDetectionWebService._internal();

  Future<void> initialize() async {
    throw UnsupportedError('Web face detection is not supported on this platform');
  }

  Future<FaceDetectionResult> detectFaces(Uint8List imageBytes) async {
    throw UnsupportedError('Web face detection is not supported on this platform');
  }

  Future<FaceValidationResult> validateFaceImage(Uint8List imageBytes) async {
    throw UnsupportedError('Web face detection is not supported on this platform');
  }

  Map<String, FaceRect> getSkinAnalysisZones(DetectedFace face) {
    throw UnsupportedError('Web face detection is not supported on this platform');
  }

  void dispose() {}
}
