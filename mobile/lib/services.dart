/// Skincare AI App - Services Barrel File
///
/// This file exports all services for convenient importing.
/// Usage: import 'package:skincare_ai_app/services.dart';
///
/// Zero-Cost Architecture Services:
/// - FaceDetectionService: On-device face detection with ML Kit (mobile)
/// - FaceDetectionWebService: Web-based face detection with face-api.js
/// - PlatformFaceDetection: Platform-aware face detection factory
/// - SkinAnalysisService: Zone-based skin analysis with AI
/// - DatabaseService: Local JSON database management

library services;

export 'services/face_detection_service.dart';
export 'services/skin_analysis_service.dart';
export 'services/database_service.dart';
export 'services/platform_face_detection.dart';
