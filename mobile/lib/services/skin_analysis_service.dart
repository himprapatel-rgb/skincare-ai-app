import 'dart:typed_data';
import 'dart:math';
import 'package:flutter/foundation.dart';
import 'face_detection_service.dart';

/// On-device skin analysis service
/// Analyzes skin conditions without any server calls - completely free!
class SkinAnalysisService {
  static final SkinAnalysisService _instance = SkinAnalysisService._internal();
  factory SkinAnalysisService() => _instance;
  SkinAnalysisService._internal();

  final FaceDetectionService _faceDetection = FaceDetectionService();
  bool _isInitialized = false;

  /// Initialize the skin analyzer
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    await _faceDetection.initialize();
    // TensorFlow Lite model will be loaded here
    _isInitialized = true;
    debugPrint('SkinAnalysisService: Initialized on-device skin analysis');
  }

  /// Analyze skin from image bytes
  /// Returns comprehensive skin analysis results
  /// CRITICAL: First validates that a face is present in the image
  Future<SkinAnalysisResult> analyzeImage(Uint8List imageBytes) async {
    if (!_isInitialized) {
      await initialize();
    }

    try {
      // STEP 1: Validate face is present using ML Kit
      final faceResult = await _faceDetection.detectFaces(imageBytes);
      
      // NO FACE DETECTED - Return error immediately
      if (!faceResult.success || faceResult.faces.isEmpty) {
        debugPrint('SkinAnalysisService: NO FACE DETECTED - Rejecting image');
        return SkinAnalysisResult.noFaceDetected(
          faceResult.errorMessage ?? 'No face detected in image. Please upload a clear selfie.',
        );
      }

      debugPrint('SkinAnalysisService: Face validated, proceeding with analysis');
      
      final face = faceResult.faces.first;
      final zones = _faceDetection.getSkinAnalysisZones(face);

      // Analyze each zone (simulated for now, will use TFLite)
      final zoneResults = <String, ZoneAnalysis>{};
      
      for (final entry in zones.entries) {
        zoneResults[entry.key] = await _analyzeZone(
          imageBytes,
          entry.value,
          entry.key,
        );
      }

      // Calculate overall metrics
      final metrics = _calculateOverallMetrics(zoneResults);

      return SkinAnalysisResult(
        success: true,
        overallScore: metrics['overallScore']!,
        hydration: metrics['hydration']!,
        oiliness: metrics['oiliness']!,
        elasticity: metrics['elasticity']!,
        pores: metrics['pores']!,
        wrinkles: metrics['wrinkles']!,
        darkSpots: metrics['darkSpots']!,
        zoneAnalysis: zoneResults,
        detectedConditions: _detectConditions(metrics),
        recommendations: _generateRecommendations(metrics),
      );
    } catch (e) {
      debugPrint('SkinAnalysisService Error: $e');
      return SkinAnalysisResult.error(e.toString());
    }
  }

  /// Analyze a specific face zone
  Future<ZoneAnalysis> _analyzeZone(
    Uint8List imageBytes,
    FaceRect zone,
    String zoneName,
  ) async {
    // Simulated analysis - will be replaced with TFLite model
    final random = Random();
    
    return ZoneAnalysis(
      zoneName: zoneName,
      texture: 60 + random.nextInt(30).toDouble(),
      hydration: 50 + random.nextInt(40).toDouble(),
      oilLevel: 30 + random.nextInt(50).toDouble(),
      pigmentation: 10 + random.nextInt(30).toDouble(),
    );
  }

  /// Calculate overall skin metrics from zone analyses
  Map<String, double> _calculateOverallMetrics(
    Map<String, ZoneAnalysis> zones,
  ) {
    if (zones.isEmpty) {
      return {
        'overallScore': 50.0,
        'hydration': 50.0,
        'oiliness': 50.0,
        'elasticity': 50.0,
        'pores': 50.0,
        'wrinkles': 20.0,
        'darkSpots': 15.0,
      };
    }

    double totalHydration = 0;
    double totalOil = 0;
    double totalTexture = 0;
    double totalPigmentation = 0;

    for (final zone in zones.values) {
      totalHydration += zone.hydration;
      totalOil += zone.oilLevel;
      totalTexture += zone.texture;
      totalPigmentation += zone.pigmentation;
    }

    final count = zones.length.toDouble();
    final avgHydration = totalHydration / count;
    final avgOil = totalOil / count;
    final avgTexture = totalTexture / count;
    final avgPigmentation = totalPigmentation / count;

    // Calculate derived metrics
    final elasticity = (avgHydration * 0.6 + avgTexture * 0.4).clamp(0.0, 100.0);
    final pores = (100 - avgOil * 0.5 - avgTexture * 0.3).clamp(0.0, 100.0);
    final wrinkles = (100 - elasticity * 0.7 - avgHydration * 0.3).clamp(0.0, 100.0);
    final darkSpots = avgPigmentation;

    // Overall score
    final overallScore = (
      avgHydration * 0.25 +
      (100 - avgOil.abs()) * 0.15 +
      elasticity * 0.2 +
      (100 - pores) * 0.15 +
      (100 - wrinkles) * 0.15 +
      (100 - darkSpots) * 0.1
    ).clamp(0.0, 100.0);

    return {
      'overallScore': overallScore,
      'hydration': avgHydration,
      'oiliness': avgOil,
      'elasticity': elasticity,
      'pores': pores,
      'wrinkles': wrinkles,
      'darkSpots': darkSpots,
    };
  }

  /// Detect skin conditions based on metrics
  List<String> _detectConditions(Map<String, double> metrics) {
    final conditions = <String>[];

    if (metrics['hydration']! < 40) conditions.add('Dehydration');
    if (metrics['oiliness']! > 70) conditions.add('Excess Oil');
    if (metrics['pores']! > 60) conditions.add('Enlarged Pores');
    if (metrics['wrinkles']! > 40) conditions.add('Fine Lines');
    if (metrics['darkSpots']! > 30) conditions.add('Hyperpigmentation');
    if (metrics['elasticity']! < 50) conditions.add('Loss of Elasticity');

    return conditions;
  }

  /// Generate product recommendations
  List<String> _generateRecommendations(Map<String, double> metrics) {
    final recommendations = <String>[];

    if (metrics['hydration']! < 50) {
      recommendations.add('Use a hyaluronic acid serum');
      recommendations.add('Apply moisturizer twice daily');
    }
    if (metrics['oiliness']! > 60) {
      recommendations.add('Use oil-free products');
      recommendations.add('Try niacinamide serum');
    }
    if (metrics['wrinkles']! > 30) {
      recommendations.add('Consider retinol treatment');
      recommendations.add('Use vitamin C serum');
    }
    if (metrics['darkSpots']! > 25) {
      recommendations.add('Apply vitamin C brightening serum');
      recommendations.add('Use SPF 50 daily');
    }

    if (recommendations.isEmpty) {
      recommendations.add('Maintain your current routine');
      recommendations.add('Always use sunscreen');
    }

    return recommendations;
  }

  void dispose() {
    _faceDetection.dispose();
    _isInitialized = false;
  }
}

/// Results from skin analysis
class SkinAnalysisResult {
  final bool success;
  final String? errorMessage;
  final double overallScore;
  final double hydration;
  final double oiliness;
  final double elasticity;
  final double pores;
  final double wrinkles;
  final double darkSpots;
  final Map<String, ZoneAnalysis> zoneAnalysis;
  final List<String> detectedConditions;
  final List<String> recommendations;

  SkinAnalysisResult({
    required this.success,
    this.errorMessage,
    this.overallScore = 0,
    this.hydration = 0,
    this.oiliness = 0,
    this.elasticity = 0,
    this.pores = 0,
    this.wrinkles = 0,
    this.darkSpots = 0,
    this.zoneAnalysis = const {},
    this.detectedConditions = const [],
    this.recommendations = const [],
  });

  factory SkinAnalysisResult.noFaceDetected([String? message]) {
    return SkinAnalysisResult(
      success: false,
      errorMessage: message ?? 'No face detected in image. Please upload a clear selfie with your face visible.',
    );
  }

  factory SkinAnalysisResult.error(String message) {
    return SkinAnalysisResult(
      success: false,
      errorMessage: message,
    );
  }
  
  /// Check if this result indicates no face was detected
  bool get isNoFaceError => !success && (errorMessage?.toLowerCase().contains('face') ?? false);
}

/// Analysis results for a specific face zone
class ZoneAnalysis {
  final String zoneName;
  final double texture;
  final double hydration;
  final double oilLevel;
  final double pigmentation;

  ZoneAnalysis({
    required this.zoneName,
    required this.texture,
    required this.hydration,
    required this.oilLevel,
    required this.pigmentation,
  });
}
