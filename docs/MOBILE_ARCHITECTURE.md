# Mobile App Architecture

## Overview
**Status:** Production-Ready  
**Framework:** Flutter 3.13+  
**Platforms:** iOS 12.0+, Android API 21+  
**Version:** 0.1.0

---

## Architecture Layers

### 1. **Presentation Layer**
- **Screens:** User-facing UI components
- **Widgets:** Reusable UI building blocks
- **State Management:** Provider pattern for reactive UI

### 2. **Business Logic Layer**
- **Services:** API calls, processing, algorithms
- **Providers:** State management (Provider/Riverpod)
- **Models:** Data transformation and validation

### 3. **Data Layer**
- **Local Storage:** SQLite (primary), Hive (cache)
- **Remote API:** Dio + Retrofit for HTTP requests
- **Repositories:** Data access abstraction

### 4. **Utility Layer**
- **Helpers:** Common functions
- **Constants:** App-wide constants
- **Formatters:** Data formatting utilities

---

## Project Structure

```
mobile/
├── lib/
│   ├── main.dart                    # App entry point
│   ├── screens/
│   │   ├── home_screen.dart         # Home/Dashboard
│   │   ├── camera_screen.dart       # Camera capture
│   │   ├── upload_screen.dart       # Image upload
│   │   ├── results_screen.dart      # Analysis results
│   │   └── history_screen.dart      # Past analyses
│   ├── widgets/
│   │   ├── camera_widget.dart       # Camera UI
│   │   ├── image_picker_widget.dart # Image selection
│   │   └── result_card.dart         # Result display
│   ├── models/
│   │   ├── skin_analysis.dart       # Analysis data model
│   │   ├── recommendation.dart      # Product recommendation
│   │   └── user_profile.dart        # User data model
│   ├── services/
│   │   ├── api_service.dart         # REST API calls
│   │   ├── camera_service.dart      # Camera operations
│   │   ├── storage_service.dart     # Local storage
│   │   └── ml_service.dart          # ML model inference
│   ├── providers/
│   │   ├── analysis_provider.dart   # Analysis state
│   │   ├── user_provider.dart       # User state
│   │   └── history_provider.dart    # History state
│   ├── repositories/
│   │   ├── analysis_repository.dart # Analysis data access
│   │   └── user_repository.dart     # User data access
│   ├── utils/
│   │   ├── constants.dart           # App constants
│   │   ├── formatters.dart          # Data formatters
│   │   ├── validators.dart          # Input validation
│   │   └── helpers.dart             # Helper functions
│   └── config/
│       ├── theme.dart               # UI theme
│       ├── routes.dart              # Navigation routes
│       └── api_config.dart          # API configuration
├── test/
│   ├── widget_test.dart             # Widget tests
│   ├── unit/
│   │   ├── models_test.dart         # Model tests
│   │   ├── services_test.dart       # Service tests
│   │   └── formatters_test.dart     # Formatter tests
│   └── integration_test/
│       ├── app_test.dart            # App flow tests
│       └── camera_test.dart         # Camera integration
├── pubspec.yaml                     # Dependencies
├── analysis_options.yaml            # Linting rules
├── SETUP_IOS_ANDROID.md            # Setup guide
├── README.md                        # Overview
└── scripts/
    ├── setup.sh                     # Setup automation
    ├── deploy_test.sh               # Deploy automation
    └── run_tests.sh                 # Test automation
```

---

## State Management: Provider Pattern

### Consumer Widget
```dart
Consumer(
  builder: (context, ref, child) {
    final analysis = ref.watch(analysisProvider);
    return Text(analysis.status);
  },
)
```

### Notifier Provider
```dart
final analysisProvider = StateNotifierProvider(
  (ref) => AnalysisNotifier(),
);

class AnalysisNotifier extends StateNotifier<Analysis> {
  AnalysisNotifier() : super(Analysis());
  
  void updateAnalysis(Analysis data) {
    state = data;
  }
}
```

---

## Data Models

### SkinAnalysis
```dart
class SkinAnalysis {
  final String id;
  final String imageUrl;
  final Map<String, double> conditions;  // acne: 0.85, wrinkles: 0.2
  final List<Recommendation> recommendations;
  final DateTime createdAt;
}
```

### Recommendation
```dart
class Recommendation {
  final String productName;
  final String category;  // cleanser, moisturizer, sunscreen
  final double confidence;
  final String reason;
  final String productLink;
}
```

---

## API Integration

### REST Endpoints
```
POST   /api/v1/analyze        # Analyze skin image
GET    /api/v1/history        # Get analysis history
GET    /api/v1/recommendations/{id}  # Get recommendations
POST   /api/v1/feedback       # Send feedback
```

### API Service Example
```dart
class ApiService {
  Future<SkinAnalysis> analyzeSkinImage(File image) async {
    var formData = FormData.fromMap({
      'image': await MultipartFile.fromFile(
        image.path,
        filename: 'skin_image.jpg',
      ),
    });
    
    final response = await dio.post(
      '/analyze',
      data: formData,
    );
    
    return SkinAnalysis.fromJson(response.data);
  }
}
```

---

## Local Storage

### SQLite for Persistent Data
- User profiles
- Analysis history
- Cached recommendations

### Hive for Fast Cache
- Recent analyses
- App preferences
- Session data

---

## Navigation

### Named Routes
```dart
MaterialApp(
  routes: {
    '/': (context) => const HomeScreen(),
    '/camera': (context) => const CameraScreen(),
    '/results': (context) => const ResultsScreen(),
    '/history': (context) => const HistoryScreen(),
  },
)
```

### Programmatic Navigation
```dart
Navigator.pushNamed(context, '/results');
Navigator.pop(context);
```

---

## Testing Strategy

### Unit Tests (40%)
- Model serialization/deserialization
- Business logic
- Utilities and formatters

### Widget Tests (40%)
- UI rendering
- User interactions
- State changes

### Integration Tests (20%)
- Full user workflows
- Camera integration
- API calls

---

## Performance Considerations

### Image Optimization
- Compress before upload (max 5MB)
- Cache compressed versions locally
- Use lazy loading for history

### Memory Management
- Dispose of controllers properly
- Clear cached images periodically
- Limit history to last 100 analyses

### Network Optimization
- Implement request timeout (30s)
- Retry on network failure (3 attempts)
- Cache API responses (1 hour)

---

## Security

### API Security
- Use HTTPS only
- Implement token-based auth (JWT)
- Validate SSL certificates

### Data Security
- Encrypt sensitive data at rest
- Secure local storage with Keychain (iOS) / Keystore (Android)
- Never log sensitive information

### Permissions
- Camera: Request on first use
- Photo Library: Request on first use
- Location: Not required initially

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Build & Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test
      - run: flutter build apk --debug
```

---

## Dependencies Overview

### State Management
- provider: UI state management
- riverpod: Advanced state management

### Networking
- dio: HTTP client
- retrofit: Type-safe REST client

### Storage
- sqflite: SQLite database
- hive: NoSQL cache
- shared_preferences: Key-value storage

### UI
- flutter_svg: SVG rendering
- shimmer: Loading shimmer effect
- cached_network_image: Image caching

### Utilities
- intl: Internationalization
- logger: Logging
- device_info_plus: Device information

---

## Future Enhancements

1. **Offline Support**
   - Service workers for API fallback
   - Sync when back online

2. **Advanced Features**
   - Augmented Reality preview
   - Video analysis
   - Personalized tracking

3. **Performance**
   - On-device ML inference
   - Image optimization
   - Bandwidth reduction

4. **Analytics**
   - User behavior tracking
   - Crash reporting
   - Performance monitoring

---

## References

- [Flutter Architecture Best Practices](https://flutter.dev/docs)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [MVVM Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)
