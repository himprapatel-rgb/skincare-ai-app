import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/foundation.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';

/// On-device face detection service using Google ML Kit
/// This runs entirely on the user's device - no server costs!
/// CRITICAL: Validates that uploaded images contain actual faces
class FaceDetectionService {
  static final FaceDetectionService _instance = FaceDetectionService._internal();
  factory FaceDetectionService() => _instance;
  FaceDetectionService._internal();

  FaceDetector? _faceDetector;
  bool _isInitialized = false;

  /// Initialize the face detector with ML Kit
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    final options = FaceDetectorOptions(
      enableContours: true,
      enableLandmarks: true,
      enableClassification: true,
      enableTracking: false,
      minFaceSize: 0.15, // Minimum face size as proportion of image
      performanceMode: FaceDetectorMode.accurate,
    );
    
    _faceDetector = FaceDetector(options: options);
    _isInitialized = true;
    debugPrint('FaceDetectionService: Initialized ML Kit face detection');
  }

  /// Detect faces in an image
  /// Returns list of detected face regions with landmarks
  /// Returns EMPTY LIST if no face is detected - UI should handle this!
  Future<FaceDetectionResult> detectFaces(Uint8List imageBytes) async {
    if (!_isInitialized) {
      await initialize();
    }

    try {
      // Create InputImage from bytes
      final inputImage = InputImage.fromBytes(
        bytes: imageBytes,
        metadata: InputImageMetadata(
          size: const ui.Size(1080, 1920), // Will be updated with actual size
          rotation: InputImageRotation.rotation0deg,
          format: InputImageFormat.nv21,
          bytesPerRow: 1080,
        ),
      );

      // Perform face detection with ML Kit
      final List<Face> faces = await _faceDetector!.processImage(inputImage);
      
      // NO FACE DETECTED - Return error result
      if (faces.isEmpty) {
        debugPrint('FaceDetectionService: NO FACE DETECTED in image');
        return FaceDetectionResult(
          success: false,
          errorMessage: 'No face detected! Please upload a clear photo of your face for skin analysis.',
          faces: [],
        );
      }

      // Convert ML Kit faces to our DetectedFace format
      final detectedFaces = faces.map((face) {
        final boundingBox = face.boundingBox;
        
        return DetectedFace(
          boundingBox: FaceRect(
            x: boundingBox.left,
            y: boundingBox.top,
            width: boundingBox.width,
            height: boundingBox.height,
          ),
          landmarks: _extractLandmarks(face),
          headEulerAngleY: face.headEulerAngleY ?? 0.0,
          headEulerAngleZ: face.headEulerAngleZ ?? 0.0,
          smilingProbability: face.smilingProbability,
          leftEyeOpenProbability: face.leftEyeOpenProbability,
          rightEyeOpenProbability: face.rightEyeOpenProbability,
        );
      }).toList();

      debugPrint('FaceDetectionService: Detected ${detectedFaces.length} face(s)');
      
      return FaceDetectionResult(
        success: true,
        errorMessage: null,
        faces: detectedFaces,
      );
      
    } catch (e) {
      debugPrint('FaceDetectionService Error: $e');
      return FaceDetectionResult(
        success: false,
        errorMessage: 'Failed to analyze image. Please try again with a different photo.',
        faces: [],
      );
    }
  }

  /// Extract landmarks from ML Kit Face
  Map<String, FacePoint> _extractLandmarks(Face face) {
    final landmarks = <String, FacePoint>{};
    
    final landmarkTypes = {
      FaceLandmarkType.leftEye: 'leftEye',
      FaceLandmarkType.rightEye: 'rightEye',
      FaceLandmarkType.noseBase: 'nose',
      FaceLandmarkType.leftCheek: 'leftCheek',
      FaceLandmarkType.rightCheek: 'rightCheek',
      FaceLandmarkType.bottomMouth: 'chin',
    };
    
    landmarkTypes.forEach((type, name) {
      final landmark = face.landmarks[type];
      if (landmark != null) {
        landmarks[name] = FacePoint(x: landmark.position.x, y: landmark.position.y);
      }
    });
    
    return landmarks;
  }

  /// Validate if image contains a suitable face for skin analysis
  Future<FaceValidationResult> validateFaceImage(Uint8List imageBytes) async {
    final result = await detectFaces(imageBytes);
    
    if (!result.success || result.faces.isEmpty) {
      return FaceValidationResult(
        isValid: false,
        message: result.errorMessage ?? 'No face detected in the image.',
        validationType: FaceValidationType.noFaceDetected,
      );
    }
    
    final face = result.faces.first;
    
    // Check if face is too tilted
    if ((face.headEulerAngleY?.abs() ?? 0) > 30) {
      return FaceValidationResult(
        isValid: false,
        message: 'Please face the camera directly. Your face appears to be turned to the side.',
        validationType: FaceValidationType.faceTooTilted,
      );
    }
    
    // Check if face is too small (likely too far from camera)
    if (face.boundingBox.width < 100 || face.boundingBox.height < 100) {
      return FaceValidationResult(
        isValid: false,
        message: 'Please move closer to the camera for better analysis.',
        validationType: FaceValidationType.faceTooSmall,
      );
    }
    
    return FaceValidationResult(
      isValid: true,
      message: 'Face detected successfully!',
      validationType: FaceValidationType.valid,
    );
  }

  /// Get face regions for skin analysis
  Map<String, FaceRect> getSkinAnalysisZones(DetectedFace face) {
    final box = face.boundingBox;
    
    return {
      'forehead': FaceRect(
        x: box.x + box.width * 0.2,
        y: box.y,
        width: box.width * 0.6,
        height: box.height * 0.2,
      ),
      'leftCheek': FaceRect(
        x: box.x,
        y: box.y + box.height * 0.3,
        width: box.width * 0.3,
        height: box.height * 0.3,
      ),
      'rightCheek': FaceRect(
        x: box.x + box.width * 0.7,
        y: box.y + box.height * 0.3,
        width: box.width * 0.3,
        height: box.height * 0.3,
      ),
      'nose': FaceRect(
        x: box.x + box.width * 0.35,
        y: box.y + box.height * 0.35,
        width: box.width * 0.3,
        height: box.height * 0.25,
      ),
      'chin': FaceRect(
        x: box.x + box.width * 0.25,
        y: box.y + box.height * 0.75,
        width: box.width * 0.5,
        height: box.height * 0.2,
      ),
    };
  }

  /// Dispose resources
  void dispose() {
    _faceDetector?.close();
    _faceDetector = null;
    _isInitialized = false;
  }
}

/// Result of face detection operation
class FaceDetectionResult {
  final bool success;
  final String? errorMessage;
  final List<DetectedFace> faces;
  
  FaceDetectionResult({
    required this.success,
    this.errorMessage,
    required this.faces,
  });
  
  bool get hasFaces => faces.isNotEmpty;
}

/// Result of face validation
class FaceValidationResult {
  final bool isValid;
  final String message;
  final FaceValidationType validationType;
  
  FaceValidationResult({
    required this.isValid,
    required this.message,
    required this.validationType,
  });
}

/// Types of validation failures
enum FaceValidationType {
  valid,
  noFaceDetected,
  faceTooSmall,
  faceTooTilted,
  multipleFaces,
  poorLighting,
}

/// Represents a detected face with bounding box and landmarks
class DetectedFace {
  final FaceRect boundingBox;
  final Map<String, FacePoint> landmarks;
  final double? headEulerAngleY;
  final double? headEulerAngleZ;
  final double? smilingProbability;
  final double? leftEyeOpenProbability;
  final double? rightEyeOpenProbability;

  DetectedFace({
    required this.boundingBox,
    required this.landmarks,
    this.headEulerAngleY,
    this.headEulerAngleZ,
    this.smilingProbability,
    this.leftEyeOpenProbability,
    this.rightEyeOpenProbability,
  });
}

/// Rectangle for face bounding box
class FaceRect {
  final double x;
  final double y;
  final double width;
  final double height;

  FaceRect({
    required this.x,
    required this.y,
    required this.width,
    required this.height,
  });
}

/// Point for face landmarks
class FacePoint {
  final double x;
  final double y;

  FacePoint({required this.x, required this.y});
}
