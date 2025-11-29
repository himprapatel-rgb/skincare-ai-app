# Zero-Cost Architecture Guide

## Overview

This document outlines how to build and deploy the Skincare AI Super App across **Web, iOS, and Android** with **zero hosting costs**.

## Architecture Diagram

```
+------------------+     +------------------+     +------------------+
|   Web (Flutter)  |     |  iOS (Flutter)   |     | Android (Flutter)|
|  GitHub Pages    |     |   App Store      |     |  Google Play     |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                    +-------------+-------------+
                    |    On-Device Processing   |
                    +-------------+-------------+
                                  |
         +------------------------+------------------------+
         |                        |                        |
+--------+---------+   +----------+----------+   +---------+--------+
|   MediaPipe      |   |   TensorFlow Lite   |   |   JSON Database  |
|   Face Mesh      |   |   Skin Analysis     |   |   (Bundled)      |
+------------------+   +---------------------+   +------------------+
```

## Platform-Specific Zero-Cost Strategy

### Web (Already Deployed)
| Component | Solution | Cost |
|-----------|----------|------|
| Hosting | GitHub Pages | FREE |
| CI/CD | GitHub Actions | FREE |
| Database | JSON files in repo | FREE |
| Face Detection | MediaPipe WASM | FREE |
| Skin Analysis | TensorFlow.js | FREE |

### iOS App
| Component | Solution | Cost |
|-----------|----------|------|
| Development | Flutter (open source) | FREE |
| Face Detection | MediaPipe iOS SDK | FREE |
| Skin Analysis | TensorFlow Lite | FREE |
| Database | Bundled JSON + SQLite | FREE |
| App Store | Apple Developer Program | $99/year* |

*Note: Required for App Store distribution only

### Android App
| Component | Solution | Cost |
|-----------|----------|------|
| Development | Flutter (open source) | FREE |
| Face Detection | MediaPipe Android SDK | FREE |
| Skin Analysis | TensorFlow Lite | FREE |
| Database | Bundled JSON + SQLite | FREE |
| Play Store | Google Play Console | $25 one-time* |

*Note: Required for Play Store distribution only

## On-Device AI Processing

### Why On-Device?
1. **Zero server costs** - All AI runs on user's device
2. **Privacy-first** - User photos never leave their device
3. **Offline capable** - Works without internet
4. **Fast response** - No network latency
5. **Infinite scale** - More users = no extra cost

### MediaPipe Face Mesh
```dart
// Flutter implementation for all platforms
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';

class FaceAnalyzer {
  final FaceDetector _faceDetector = FaceDetector(
    options: FaceDetectorOptions(
      enableLandmarks: true,
      enableContours: true,
      performanceMode: FaceDetectorMode.accurate,
    ),
  );
  
  Future<List<Face>> detectFaces(InputImage image) async {
    return await _faceDetector.processImage(image);
  }
}
```

### TensorFlow Lite Skin Analysis
```dart
// Cross-platform skin analysis
import 'package:tflite_flutter/tflite_flutter.dart';

class SkinAnalyzer {
  late Interpreter _interpreter;
  
  Future<void> loadModel() async {
    _interpreter = await Interpreter.fromAsset('skin_analysis_model.tflite');
  }
  
  Future<SkinAnalysisResult> analyze(Uint8List imageBytes) async {
    // Process image and return skin condition analysis
    var input = preprocessImage(imageBytes);
    var output = List.filled(5, 0.0).reshape([1, 5]);
    _interpreter.run(input, output);
    return SkinAnalysisResult.fromOutput(output);
  }
}
```

## JSON Database (Bundled with App)

Location: `backend/app/data/`

| File | Purpose | Size |
|------|---------|------|
| products.json | Skincare product catalog | ~10KB |
| skin_conditions.json | Skin condition definitions | ~5KB |
| ingredients.json | Ingredient safety database | ~8KB |

### Loading JSON Data in Flutter
```dart
import 'dart:convert';
import 'package:flutter/services.dart';

class DatabaseService {
  Map<String, dynamic>? _products;
  Map<String, dynamic>? _ingredients;
  Map<String, dynamic>? _conditions;
  
  Future<void> initialize() async {
    _products = await _loadJson('assets/data/products.json');
    _ingredients = await _loadJson('assets/data/ingredients.json');
    _conditions = await _loadJson('assets/data/skin_conditions.json');
  }
  
  Future<Map<String, dynamic>> _loadJson(String path) async {
    final String response = await rootBundle.loadString(path);
    return json.decode(response);
  }
  
  List<Product> getProductsForCondition(String condition) {
    // Match products to skin conditions using local data
  }
}
```

## Free Distribution Options

### Web
- **GitHub Pages** (current) - Unlimited traffic, FREE
- **Netlify** - 100GB/month, FREE
- **Vercel** - 100GB/month, FREE

### iOS (Without App Store)
- **TestFlight** - Up to 10,000 beta testers, FREE
- **Ad-hoc distribution** - Up to 100 devices, FREE
- **Enterprise** - Requires Apple Developer Enterprise Program

### Android (Without Play Store)
- **Direct APK download** - Host on GitHub Releases, FREE
- **F-Droid** - Open source app store, FREE
- **Amazon Appstore** - FREE to publish
- **Samsung Galaxy Store** - FREE to publish

## Build Commands

### Web (GitHub Pages)
```bash
flutter build web --release --base-href "/skincare-ai-app/"
# Automatically deployed via GitHub Actions
```

### iOS
```bash
flutter build ios --release
# Archive and upload via Xcode
```

### Android
```bash
flutter build apk --release
flutter build appbundle --release  # For Play Store
```

## Cost Summary

| Platform | Development | Hosting | Distribution | Total |
|----------|-------------|---------|--------------|-------|
| Web | $0 | $0 (GitHub Pages) | $0 | **$0** |
| Android | $0 | $0 (bundled) | $25 one-time | **$25** |
| iOS | $0 | $0 (bundled) | $99/year | **$99/year** |

### Truly Zero-Cost Options
- **Web**: Completely free via GitHub Pages
- **Android**: APK distribution via GitHub Releases (free)
- **iOS**: TestFlight beta testing (free with Apple ID)

## Next Steps

1. [x] Set up JSON database in repo
2. [ ] Integrate MediaPipe face detection in Flutter
3. [ ] Add TensorFlow Lite skin analysis model
4. [ ] Bundle JSON data as Flutter assets
5. [ ] Test on Web, iOS Simulator, Android Emulator
6. [ ] Deploy to GitHub Pages (Web)
7. [ ] Build APK for Android testing
8. [ ] Build for iOS TestFlight

## Resources

- [MediaPipe Face Detection](https://developers.google.com/mediapipe/solutions/vision/face_detector)
- [TensorFlow Lite Flutter](https://pub.dev/packages/tflite_flutter)
- [Google ML Kit](https://pub.dev/packages/google_mlkit_face_detection)
- [Flutter Web Deployment](https://docs.flutter.dev/deployment/web)

---
*Last Updated: November 29, 2025*
