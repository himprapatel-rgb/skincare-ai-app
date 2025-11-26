#!/bin/bash
# Comprehensive iOS & Android Environment Testing Script
# Tests both platforms systematically
# Author: QA Team
# Date: 2025-11-26

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}iOS & Android Environment Test Suite${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

print_test() {
    echo -e "${YELLOW}[TEST]${NC} $1"
    ((TOTAL_TESTS++))
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED_TESTS++))
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILED_TESTS++))
}

# Phase 1: Environment Verification
echo -e "\n${BLUE}=== PHASE 1: Environment Verification ===${NC}"

print_test "Flutter installation"
if command -v flutter &> /dev/null; then
    FLUTTER_VERSION=$(flutter --version | head -n1)
    print_pass "Flutter found: $FLUTTER_VERSION"
else
    print_fail "Flutter not found"
fi

print_test "iOS SDK (Xcode)"
if command -v xcode-select &> /dev/null; then
    XCODE_PATH=$(xcode-select --print-path)
    print_pass "Xcode found at $XCODE_PATH"
else
    print_fail "Xcode not found (iOS not supported on this machine)"
fi

print_test "Android SDK"
if [ -n "$ANDROID_HOME" ]; then
    print_pass "ANDROID_HOME set to $ANDROID_HOME"
else
    print_fail "ANDROID_HOME not set"
fi

print_test "Java installation"
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n1)
    print_pass "Java found: $JAVA_VERSION"
else
    print_fail "Java not found"
fi

# Phase 2: Project Setup
echo -e "\n${BLUE}=== PHASE 2: Project Setup ===${NC}"

print_test "Navigate to mobile directory"
cd mobile
if [ -f "pubspec.yaml" ]; then
    print_pass "pubspec.yaml found"
else
    print_fail "pubspec.yaml not found"
    exit 1
fi

print_test "Clean previous builds"
flutter clean > /dev/null 2>&1 && print_pass "Flutter clean completed" || print_fail "Flutter clean failed"

print_test "Get dependencies"
if flutter pub get > /dev/null 2>&1; then
    DEPS=$(grep -c "^  " pubspec.yaml) || DEPS="20+"
    print_pass "Dependencies installed (approx $DEPS packages)"
else
    print_fail "Failed to get dependencies"
fi

# Phase 3: iOS Build Test
echo -e "\n${BLUE}=== PHASE 3: iOS Build Test ===${NC}"

print_test "iOS debug build"
if flutter build ios --debug > ios_build.log 2>&1; then
    if [ -d "build/ios" ]; then
        SIZE=$(du -sh build/ios | cut -f1)
        print_pass "iOS debug build successful (size: $SIZE)"
    else
        print_fail "iOS build directory not found"
    fi
else
    print_fail "iOS build failed (see ios_build.log)"
fi

# Phase 4: Android Build Test
echo -e "\n${BLUE}=== PHASE 4: Android Build Test ===${NC}"

print_test "Android debug APK"
if flutter build apk --debug > android_build.log 2>&1; then
    if [ -f "build/app/outputs/apk/debug/app-debug.apk" ]; then
        SIZE=$(ls -lh build/app/outputs/apk/debug/app-debug.apk | awk '{print $5}')
        print_pass "Android debug APK successful (size: $SIZE)"
    else
        print_fail "Android APK not found"
    fi
else
    print_fail "Android build failed (see android_build.log)"
fi

# Phase 5: Widget Tests
echo -e "\n${BLUE}=== PHASE 5: Widget Tests ===${NC}"

print_test "Widget test execution"
if flutter test 2>&1 | tee test_results.log | grep -q "All tests passed"; then
    print_pass "All widget tests passed"
else
    print_fail "Some widget tests failed (see test_results.log)"
fi

# Phase 6: Code Analysis
echo -e "\n${BLUE}=== PHASE 6: Code Analysis ===${NC}"

print_test "Flutter analyze"
if flutter analyze > /dev/null 2>&1; then
    print_pass "No code analysis issues"
else
    print_fail "Code analysis found issues"
fi

# Summary
echo -e "\n${BLUE}================================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}================================================${NC}"
echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
else
    echo -e "${GREEN}Failed: $FAILED_TESTS${NC}"
fi

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}✓ ALL TESTS PASSED - READY FOR DEVELOPMENT${NC}"
    exit 0
else
    echo -e "\n${RED}✗ SOME TESTS FAILED - FIX ISSUES AND RE-RUN${NC}"
    exit 1
fi
