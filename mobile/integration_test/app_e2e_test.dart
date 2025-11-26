import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:skincare_ai_app/main.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Skincare AI App E2E Tests', () {
    const String apiBaseUrl = 'http://localhost:8000/api/v1';
    late String authToken;
    late String userId;

    // Helper function to make HTTP requests
    Future<http.Response> makeRequest(
      String method,
      String endpoint, {
      Map<String, dynamic>? body,
      bool requiresAuth = true,
    }) async {
      final Uri url = Uri.parse('$apiBaseUrl$endpoint');
      final Map<String, String> headers = {
        'Content-Type': 'application/json',
        if (requiresAuth) 'Authorization': 'Bearer $authToken',
      };

      switch (method.toUpperCase()) {
        case 'POST':
          return await http.post(url, headers: headers, body: jsonEncode(body));
        case 'GET':
          return await http.get(url, headers: headers);
        case 'PUT':
          return await http.put(url, headers: headers, body: jsonEncode(body));
        case 'DELETE':
          return await http.delete(url, headers: headers);
        default:
          throw Exception('Unsupported HTTP method: $method');
      }
    }

    testWidgets('1. Authentication Test - Register and Login',
        (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());

      // Verify login screen appears
      expect(find.byType(Text), findsWidgets);

      // Test registration
      final registerResponse = await makeRequest(
        'POST',
        '/auth/register',
        body: {
          'email': 'testuser@example.com',
          'password': 'Test@1234',
          'first_name': 'Test',
          'last_name': 'User',
        },
        requiresAuth: false,
      );

      expect(registerResponse.statusCode, equals(201));
      final registerData = jsonDecode(registerResponse.body);
      print('Registration successful: ${registerData['message']}');

      // Test login
      final loginResponse = await makeRequest(
        'POST',
        '/auth/login',
        body: {
          'email': 'testuser@example.com',
          'password': 'Test@1234',
        },
        requiresAuth: false,
      );

      expect(loginResponse.statusCode, equals(200));
      final loginData = jsonDecode(loginResponse.body);
      authToken = loginData['access_token'];
      userId = loginData['user_id'];
      print('Login successful - Token: ${authToken.substring(0, 20)}...');
    });

    testWidgets('2. User Profile Integration Test',
        (WidgetTester tester) async {
      // Create user profile
      final profileResponse = await makeRequest(
        'PUT',
        '/users/$userId',
        body: {
          'skin_type': 'oily',
          'skin_concerns': ['acne', 'oiliness'],
          'age': 25,
          'gender': 'female',
        },
      );

      expect(profileResponse.statusCode, equals(200));
      print('Profile updated successfully');

      // Fetch user profile
      final getProfileResponse = await makeRequest('GET', '/users/$userId');
      expect(getProfileResponse.statusCode, equals(200));
      final profileData = jsonDecode(getProfileResponse.body);
      print('Profile data: ${profileData['skin_type']}');
    });

    testWidgets('3. Skin Analysis Integration Test',
        (WidgetTester tester) async {
      // Create a mock image for testing
      const imageBase64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';

      final analysisResponse = await makeRequest(
        'POST',
        '/analysis/analyze',
        body: {
          'image_data': imageBase64,
          'user_id': userId,
        },
      );

      expect(analysisResponse.statusCode, equals(200));
      final analysisData = jsonDecode(analysisResponse.body);
      print('Skin analysis result:');
      print('  - Condition: ${analysisData['skin_condition']}');
      print('  - Severity: ${analysisData['severity']}');
      print('  - Recommendations: ${analysisData['recommendations']}');
    });

    testWidgets('4. Ingredient Scanner Integration Test',
        (WidgetTester tester) async {
      final ingredientResponse = await makeRequest(
        'POST',
        '/ingredients/scan',
        body: {
          'product_name': 'Gentle Face Cleanser',
          'ingredients': [
            'Water',
            'Sodium Lauryl Sulfate',
            'Glycerin',
            'Vitamin C',
          ],
        },
      );

      expect(ingredientResponse.statusCode, equals(200));
      final ingredientData = jsonDecode(ingredientResponse.body);
      print('Ingredient analysis:');
      print('  - Safety rating: ${ingredientData['safety_rating']}');
      print('  - Benefits: ${ingredientData['benefits']}');
      print('  - Warnings: ${ingredientData['warnings']}');
    });

    testWidgets('5. Routine Creation Integration Test',
        (WidgetTester tester) async {
      final routineResponse = await makeRequest(
        'POST',
        '/routine/create',
        body: {
          'user_id': userId,
          'skin_type': 'oily',
          'time_commitment': 'medium',
        },
      );

      expect(routineResponse.statusCode, equals(200));
      final routineData = jsonDecode(routineResponse.body);
      final routineId = routineData['routine_id'];
      print('Routine created: $routineId');
      print('Steps: ${routineData['steps']}');

      // Fetch routine
      final getRoutineResponse = await makeRequest(
        'GET',
        '/routine/user/$userId',
      );

      expect(getRoutineResponse.statusCode, equals(200));
      final routines = jsonDecode(getRoutineResponse.body);
      print('Total routines: ${routines.length}');
    });

    testWidgets('6. Progress Tracking Integration Test',
        (WidgetTester tester) async {
      // Update progress
      final updateProgressResponse = await makeRequest(
        'POST',
        '/progress/update',
        body: {
          'user_id': userId,
          'metric': 'skin_clarity',
          'value': 8.5,
          'notes': 'Significant improvement',
        },
      );

      expect(updateProgressResponse.statusCode, equals(200));
      print('Progress updated successfully');

      // Fetch progress metrics
      final metricsResponse = await makeRequest(
        'GET',
        '/progress/metrics?user_id=$userId',
      );

      expect(metricsResponse.statusCode, equals(200));
      final metricsData = jsonDecode(metricsResponse.body);
      print('Progress metrics: $metricsData');
    });

    testWidgets('7. Notification Integration Test',
        (WidgetTester tester) async {
      // Send notification
      final notificationResponse = await makeRequest(
        'POST',
        '/notifications/push',
        body: {
          'user_id': userId,
          'title': 'Routine Reminder',
          'body': 'Time for your evening skincare routine!',
          'type': 'routine_reminder',
        },
      );

      expect(notificationResponse.statusCode, equals(200));
      print('Notification sent successfully');

      // Fetch notifications
      final getNotificationsResponse = await makeRequest(
        'GET',
        '/notifications?user_id=$userId',
      );

      expect(getNotificationsResponse.statusCode, equals(200));
      final notifications = jsonDecode(getNotificationsResponse.body);
      print('Total notifications: ${notifications.length}');
    });

    testWidgets('8. Dermatologist Consultation Integration Test',
        (WidgetTester tester) async {
      // Get available slots
      final availableResponse = await makeRequest(
        'GET',
        '/dermatologist/available?date=2024-01-15',
      );

      expect(availableResponse.statusCode, equals(200));
      final availableSlots = jsonDecode(availableResponse.body);
      print('Available consultation slots: ${availableSlots.length}');

      if (availableSlots.isNotEmpty) {
        // Book consultation
        final bookResponse = await makeRequest(
          'POST',
          '/dermatologist/book',
          body: {
            'user_id': userId,
            'slot_id': availableSlots[0]['slot_id'],
            'reason': 'Acne treatment consultation',
          },
        );

        expect(bookResponse.statusCode, equals(200));
        final bookingData = jsonDecode(bookResponse.body);
        print('Consultation booked: ${bookingData['consultation_id']}');
      }
    });

    testWidgets('9. Error Handling Test - Invalid Credentials',
        (WidgetTester tester) async {
      final response = await makeRequest(
        'POST',
        '/auth/login',
        body: {
          'email': 'invalid@example.com',
          'password': 'wrongpassword',
        },
        requiresAuth: false,
      );

      expect(response.statusCode, equals(401));
      final errorData = jsonDecode(response.body);
      print('Error handling test passed: ${errorData['detail']}');
    });

    testWidgets('10. Error Handling Test - Missing Parameters',
        (WidgetTester tester) async {
      final response = await makeRequest(
        'POST',
        '/auth/login',
        body: {'email': 'test@example.com'},
        requiresAuth: false,
      );

      expect(response.statusCode, equals(400));
      print('Parameter validation test passed');
    });

    testWidgets('11. Data Synchronization Test',
        (WidgetTester tester) async {
      // Simulate offline changes
      Map<String, dynamic> localChanges = {'preferences': {'reminder_time': '09:00'}};

      // Sync with backend when online
      final syncResponse = await makeRequest(
        'PUT',
        '/users/$userId',
        body: localChanges,
      );

      expect(syncResponse.statusCode, equals(200));
      print('Data synchronization test passed');
    });

    testWidgets('12. Complete User Workflow Test',
        (WidgetTester tester) async {
      print('\n=== COMPLETE USER WORKFLOW TEST ===');
      
      // Step 1: Profile Setup
      print('Step 1: Setting up user profile...');
      await makeRequest('PUT', '/users/$userId', body: {
        'skin_type': 'combination',
        'skin_concerns': ['acne', 'sensitivity'],
      });

      // Step 2: Skin Analysis
      print('Step 2: Performing skin analysis...');
      const imageBase64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
      final analysisRes = await makeRequest('POST', '/analysis/analyze', body: {
        'image_data': imageBase64,
        'user_id': userId,
      });
      expect(analysisRes.statusCode, equals(200));

      // Step 3: Routine Creation
      print('Step 3: Creating skincare routine...');
      final routineRes = await makeRequest('POST', '/routine/create', body: {
        'user_id': userId,
        'skin_type': 'combination',
      });
      expect(routineRes.statusCode, equals(200));

      // Step 4: Progress Tracking
      print('Step 4: Recording progress...');
      await makeRequest('POST', '/progress/update', body: {
        'user_id': userId,
        'metric': 'skin_health',
        'value': 7.5,
      });

      // Step 5: Ingredient Scanning
      print('Step 5: Scanning product ingredients...');
      await makeRequest('POST', '/ingredients/scan', body: {
        'product_name': 'Moisturizer',
        'ingredients': ['Water', 'Glycerin', 'Hyaluronic Acid'],
      });

      print('=== WORKFLOW COMPLETED SUCCESSFULLY ===\n');
    });
  });
}
