# iOS & Android Testing & Deployment Guide

## Status: Production Ready
**Last Updated:** 2025-11-26  
**Version:** 0.1.0  
**Authority:** Mobile Development Team

---

## Quick Reference

### Setup (One-Time)
```bash
cd mobile
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Run App
```bash
# Debug mode
flutter run

# Specific device
flutter run -d <device-id>

# Release mode
flutter run --release
```

### Test
```bash
# All tests
flutter test

# With coverage
flutter test --coverage
```

### Build
```bash
# iOS Debug
flutter build ios --debug

# Android Debug APK
flutter build apk --debug

# Android Release APK
flutter build apk --release

# Android App Bundle (Play Store)
flutter build appbundle --release
```

---

## iOS Testing & Deployment

### Prerequisites
- macOS 12.0+
- Xcode 14+
- CocoaPods
- iOS 12.0+ device/simulator

### iOS Simulator

#### Launch Simulator
```bash
# List available simulators
flutter emulators

# Launch default
open -a Simulator

# Via Flutter
flutter emulators --launch apple_ios_simulator
```

#### Run App on Simulator
```bash
cd mobile
flutter run

# Specific simulator
flutter run -d "iPhone 15 Pro"
```

#### Test on Simulator
```bash
flutter test
flutter test --coverage
```

### iOS Physical Device

#### Connect Device
1. Connect iPhone via USB
2. Trust the device when prompted
3. Verify connection: `flutter devices`

#### Deploy to Device
```bash
# Debug
flutter run -d <device-id>

# Release
flutter run --release -d <device-id>
```

#### Build for Device
```bash
# Debug build
flutter build ios --debug

# Release build  
flutter build ios --release

# Open in Xcode for manual deployment
open ios/Runner.xcworkspace
```

### iOS Troubleshooting

**Pod install fails:**
```bash
cd ios
rm Podfile.lock
pod install --repo-update
cd ..
```

**Code signing issues:**
- Open `ios/Runner.xcworkspace` in Xcode
- Go to Build Settings
- Select correct team and profile

**Build fails:**
```bash
flutter clean
cd ios
rm -rf Pods Podfile.lock
cd ..
flutter pub get
flutter run
```

---

## Android Testing & Deployment

### Prerequisites
- Android SDK API 21+
- Android NDK
- Java 11+
- ANDROID_HOME set

### Android Emulator

#### Create Emulator (if needed)
```bash
# Via Android Studio AVD Manager
# OR via command line
flutter emulators --create --name "test_device"
```

#### Launch Emulator
```bash
# List emulators
flutter emulators

# Launch
flutter emulators --launch Pixel_5_API_33

# Wait for emulator to fully boot
flutter devices
```

#### Run App on Emulator
```bash
cd mobile
flutter run

# Specific emulator
flutter run -d emulator-5554
```

#### Test on Emulator
```bash
flutter test
flutter test --coverage
```

### Android Physical Device

#### Enable USB Debugging
1. Connect Android phone via USB
2. Go to Settings > About Phone
3. Tap Build Number 7 times
4. Go to Developer Options
5. Enable USB Debugging
6. Trust computer when prompted

#### Verify Connection
```bash
flutter devices
adb devices
```

#### Deploy to Device
```bash
# Debug
flutter run -d <device-id>

# Release
flutter run --release -d <device-id>
```

#### Build for Device
```bash
# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release

# Install APK
adb install build/app/outputs/apk/debug/app-debug.apk
```

### Android Troubleshooting

**ADB not found:**
```bash
export PATH=$PATH:$ANDROID_HOME/platform-tools
adb devices
```

**Gradle build fails:**
```bash
cd android
./gradlew clean build
cd ..
```

**Emulator won't start:**
```bash
# Check available emulators
flutter emulators

# Launch with more memory
flutter emulators --launch <name>

# Or via command line
emulator -avd <name> -memory 2048
```

**Installation fails on device:**
```bash
# Clear old app
adb uninstall com.skincareai.app

# Reinstall
flutter install -d <device-id>
```

---

## Testing Workflow

### Unit Tests
```bash
# Run unit tests
flutter test test/unit/

# Watch mode
flutter test --watch
```

### Widget Tests
```bash
# Run widget tests
flutter test test/widget_test.dart

# All tests
flutter test
```

### Integration Tests
```bash
# Run integration tests
flutter test integration_test/

# On device
flutter test integration_test/ -d <device-id>
```

### Coverage Report
```bash
# Generate coverage
flutter test --coverage

# View coverage (macOS/Linux)
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

## Build & Release

### Pre-Release Checklist
- [ ] All tests passing
- [ ] No linting errors: `flutter analyze`
- [ ] Code coverage >= 80%
- [ ] No console errors
- [ ] Performance acceptable
- [ ] UI looks correct on both platforms
- [ ] Camera works
- [ ] Image upload works
- [ ] API calls succeed
- [ ] Version updated in `pubspec.yaml`

### iOS Release
```bash
# Build for release
flutter build ios --release

# Archive for App Store
open ios/Runner.xcworkspace
# In Xcode: Product > Archive
```

### Android Release
```bash
# Build Release APK
flutter build apk --release

# Build App Bundle (for Play Store)
flutter build appbundle --release

# Outputs:
# APK: build/app/outputs/apk/release/app-release.apk
# AAB: build/app/outputs/bundle/release/app-release.aab
```

---

## Performance Optimization

### Profile Build
```bash
# Build profile version
flutter build apk --profile
flutter build ios --profile

# Run with performance monitoring
flutter run --profile
```

### Performance Testing
```bash
# Frame rate monitoring
flutter run --profile --trace-startup

# Memory profiling
flutter run --profile
# Then use Android Studio DevTools
```

---

## Automated Deployment

### Using Deployment Script
```bash
# Debug build (default)
./mobile/scripts/deploy_test.sh

# Profile build
./mobile/scripts/deploy_test.sh --profile

# Release build
./mobile/scripts/deploy_test.sh --release

# iOS only
./mobile/scripts/deploy_test.sh --ios-only

# Android only
./mobile/scripts/deploy_test.sh --android-only
```

---

## Continuous Integration

### Local Testing Before Commit
```bash
# Run full test suite
flutter test

# Build both platforms
flutter build ios --debug
flutter build apk --debug

# Then commit
git add .
git commit -m "feat: add feature"
git push
```

---

## Device Management

### List Devices
```bash
flutter devices      # Flutter devices
adb devices         # Android devices only
```

### Clear App Data
```bash
# iOS: Simulator > Settings > General > iPhone Storage
# Android
adb shell pm clear com.skincareai.app
```

### Uninstall App
```bash
# iOS
adb uninstall com.skincareai.app

# Android
flutter uninstall
```

---

## FAQ

**Q: App keeps crashing?**  
A: Check logs: `flutter run -v`. Look for error messages. Ensure all dependencies installed: `flutter pub get`

**Q: Camera not working?**  
A: Verify permissions. Check camera/microphone permissions in app settings.

**Q: Build too slow?**  
A: Use debug build (default). Release builds are optimized but slower to build.

**Q: How to debug?**  
A: `flutter run` shows full debug output. Use breakpoints in VS Code or Android Studio.

**Q: How to test on real device?**  
A: Enable developer mode, connect via USB, run `flutter run -d <device-id>`

---

## Resources

- [Flutter Testing Docs](https://flutter.dev/docs/testing)
- [Flutter Deployment Docs](https://flutter.dev/docs/deployment)
- [iOS Development](https://developer.apple.com/ios)
- [Android Development](https://developer.android.com)

---

**Next Steps:**
1. Complete setup: `./mobile/scripts/setup.sh`
2. Launch emulator/simulator
3. Run app: `flutter run`
4. Run tests: `flutter test`
5. Build for release
6. Deploy to devices