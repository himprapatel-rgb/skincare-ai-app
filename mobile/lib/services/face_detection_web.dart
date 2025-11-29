// ignore_for_file: avoid_web_libraries_in_flutter
import 'dart:async';
import 'dart:convert';
import 'dart:js' as js;
import 'dart:typed_data';

import 'package:flutter/foundation.dart';

import 'face_detection_service.dart';

/// Web implementation of face detection using face-api.js
/// This service uses JavaScript interop to communicate with the face_api_web.js library
class FaceDetectionWebService {
  static final FaceDetectionWebService _instance = FaceDetectionWebService._internal();
  factory FaceDetectionWebService() => _instance;
  FaceDetectionWebService._internal();

  bool _isInitialized = false;

  /// Initialize the face-api.js library
  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      // Check if FaceApiWeb is available
      final faceApiWeb = js.context['FaceApiWeb'];
      if (faceApiWeb == null) {
        debugPrint('FaceDetectionWebService: FaceApiWeb not found, waiting...');
        // Wait for the script to load
        await Future.delayed(const Duration(seconds: 2));
      }

      // Initialize face-api.js models
      final result = await _callJsAsync('initialize');
      _isInitialized = result == true;
      
      debugPrint('FaceDetectionWebService: Initialized = $_isInitialized');
    } catch (e) {
      debugPrint('FaceDetectionWebService initialization error: $e');
      _isInitialized = false;
    }
  }

  /// Detect faces in an image
  Future<FaceDetectionResult> detectFaces(Uint8List imageBytes) async {
    if (!_isInitialized) {
      await initialize();
    }

    try {
      // Convert image bytes to base64
      final base64Image = base64Encode(imageBytes);

      // Call JavaScript face detection
      final jsResult = await _callJsAsync('detectFaces', [base64Image]);

      if (jsResult == null) {
        return FaceDetectionResult(
          success: false,
          errorMessage: 'Face detection returned no result',
          faces: [],
        );
      }

      // Parse the result from JavaScript
      final result = _parseJsResult(jsResult);
      return result;
    } catch (e) {
      debugPrint('FaceDetectionWebService detectFaces error: $e');
      return FaceDetectionResult(
        success: false,
        errorMessage: 'Face detection failed: $e',
        faces: [],
      );
    }
  }

  /// Validate if the face is suitable for skin analysis
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

    // Check minimum face size
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

  /// Get skin analysis zones from detected face
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

  /// Call JavaScript function asynchronously
  Future<dynamic> _callJsAsync(String method, [List<dynamic>? args]) async {
    final completer = Completer<dynamic>();

    try {
      final faceApiWeb = js.context['FaceApiWeb'];
      if (faceApiWeb == null) {
        completer.completeError('FaceApiWeb not available');
        return completer.future;
      }

      final jsFunction = faceApiWeb[method];
      if (jsFunction == null) {
        completer.completeError('Method $method not found');
        return completer.future;
      }

      // Call the JavaScript function
      final jsArgs = args?.map((a) => js.JsObject.jsify(a is Map || a is List ? a : a)).toList();
      final result = jsArgs != null && jsArgs.isNotEmpty
          ? jsFunction.apply(jsArgs)
          : jsFunction.apply([]);

      // Handle Promise
      if (result is js.JsObject && result.hasProperty('then')) {
        result.callMethod('then', [
          js.allowInterop((value) => completer.complete(value)),
        ]);
        result.callMethod('catch', [
          js.allowInterop((error) => completer.completeError(error.toString())),
        ]);
      } else {
        completer.complete(result);
      }
    } catch (e) {
      completer.completeError(e);
    }

    return completer.future;
  }

  /// Parse JavaScript result to Dart FaceDetectionResult
  FaceDetectionResult _parseJsResult(dynamic jsResult) {
    try {
      // Convert JsObject to Dart Map
      final resultMap = _jsObjectToMap(jsResult);

      final success = resultMap['success'] as bool? ?? false;
      final errorMessage = resultMap['errorMessage'] as String?;
      final facesData = resultMap['faces'] as List? ?? [];

      final faces = facesData.map((faceData) {
        final faceMap = faceData is Map ? faceData : _jsObjectToMap(faceData);
        final boxData = faceMap['boundingBox'] is Map
            ? faceMap['boundingBox'] as Map
            : _jsObjectToMap(faceMap['boundingBox']);

        return DetectedFace(
          boundingBox: FaceRect(
            x: (boxData['x'] as num?)?.toDouble() ?? 0,
            y: (boxData['y'] as num?)?.toDouble() ?? 0,
            width: (boxData['width'] as num?)?.toDouble() ?? 0,
            height: (boxData['height'] as num?)?.toDouble() ?? 0,
          ),
          landmarks: _parseLandmarks(faceMap['landmarks']),
          headEulerAngleY: 0.0,
          headEulerAngleZ: 0.0,
        );
      }).toList();

      return FaceDetectionResult(
        success: success,
        errorMessage: errorMessage,
        faces: faces,
      );
    } catch (e) {
      debugPrint('Error parsing JS result: $e');
      return FaceDetectionResult(
        success: false,
        errorMessage: 'Failed to parse detection result',
        faces: [],
      );
    }
  }

  /// Convert JsObject to Dart Map
  Map<String, dynamic> _jsObjectToMap(dynamic jsObject) {
    if (jsObject == null) return {};
    if (jsObject is Map) return Map<String, dynamic>.from(jsObject);

    try {
      // Use JSON stringify/parse for conversion
      final jsonString = js.context['JSON'].callMethod('stringify', [jsObject]);
      return jsonDecode(jsonString as String) as Map<String, dynamic>;
    } catch (e) {
      debugPrint('Error converting JsObject to Map: $e');
      return {};
    }
  }

  /// Parse landmarks from JavaScript result
  Map<String, FacePoint> _parseLandmarks(dynamic landmarksData) {
    if (landmarksData == null) return {};

    final landmarks = <String, FacePoint>{};
    final landmarksMap = landmarksData is Map
        ? landmarksData
        : _jsObjectToMap(landmarksData);

    final landmarkNames = ['leftEye', 'rightEye', 'nose', 'leftCheek', 'rightCheek'];

    for (final name in landmarkNames) {
      final point = landmarksMap[name];
      if (point != null) {
        final pointMap = point is Map ? point : _jsObjectToMap(point);
        landmarks[name] = FacePoint(
          x: (pointMap['x'] as num?)?.toDouble() ?? 0,
          y: (pointMap['y'] as num?)?.toDouble() ?? 0,
        );
      }
    }

    return landmarks;
  }

  void dispose() {
    _isInitialized = false;
  }
}
