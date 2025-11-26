#!/bin/bash
# Run all tests for iOS and Android

set -e

echo "================================================"
echo "Running All Tests"
echo "================================================"
echo ""

echo "[*] Running Flutter unit tests..."
flutter test

echo ""
echo "[*] Running Flutter widget tests..."
flutter test test/widget_test.dart || true

echo ""
echo "[*] Generating coverage report..."
flutter test --coverage || true

echo ""
echo "================================================"
echo "All tests complete!"
echo "================================================"
