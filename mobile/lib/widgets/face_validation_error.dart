import 'package:flutter/material.dart';
import '../services/face_detection_service.dart';

/// Widget to display face validation errors
/// Shows user-friendly messages when face detection fails
class FaceValidationError extends StatelessWidget {
  final FaceValidationResult validationResult;
  final VoidCallback onRetry;

  const FaceValidationError({
    super.key,
    required this.validationResult,
    required this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Error Icon
          Container(
            width: 120,
            height: 120,
            decoration: BoxDecoration(
              color: _getIconBackgroundColor(),
              shape: BoxShape.circle,
            ),
            child: Icon(
              _getIcon(),
              size: 60,
              color: _getIconColor(),
            ),
          ),
          const SizedBox(height: 24),

          // Error Title
          Text(
            _getTitle(),
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: Colors.grey[800],
                ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 12),

          // Error Message
          Text(
            validationResult.message,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: Colors.grey[600],
                ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),

          // Helpful Tip
          Container(
            padding: const EdgeInsets.all(16),
            margin: const EdgeInsets.symmetric(vertical: 16),
            decoration: BoxDecoration(
              color: Colors.blue[50],
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.blue[200]!),
            ),
            child: Row(
              children: [
                Icon(Icons.lightbulb_outline, color: Colors.blue[600]),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    _getHelpfulTip(),
                    style: TextStyle(
                      color: Colors.blue[800],
                      fontSize: 14,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Retry Button
          ElevatedButton.icon(
            onPressed: onRetry,
            icon: const Icon(Icons.camera_alt),
            label: const Text('Try Again'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              backgroundColor: Theme.of(context).primaryColor,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30),
              ),
            ),
          ),
        ],
      ),
    );
  }

  IconData _getIcon() {
    switch (validationResult.validationType) {
      case FaceValidationType.noFaceDetected:
        return Icons.face_retouching_off;
      case FaceValidationType.faceTooSmall:
        return Icons.zoom_in;
      case FaceValidationType.faceTooTilted:
        return Icons.screen_rotation;
      case FaceValidationType.multipleFaces:
        return Icons.people_outline;
      case FaceValidationType.poorLighting:
        return Icons.wb_sunny_outlined;
      default:
        return Icons.error_outline;
    }
  }

  Color _getIconColor() {
    switch (validationResult.validationType) {
      case FaceValidationType.noFaceDetected:
        return Colors.red[600]!;
      case FaceValidationType.faceTooSmall:
        return Colors.orange[600]!;
      case FaceValidationType.faceTooTilted:
        return Colors.amber[600]!;
      default:
        return Colors.red[600]!;
    }
  }

  Color _getIconBackgroundColor() {
    switch (validationResult.validationType) {
      case FaceValidationType.noFaceDetected:
        return Colors.red[50]!;
      case FaceValidationType.faceTooSmall:
        return Colors.orange[50]!;
      case FaceValidationType.faceTooTilted:
        return Colors.amber[50]!;
      default:
        return Colors.red[50]!;
    }
  }

  String _getTitle() {
    switch (validationResult.validationType) {
      case FaceValidationType.noFaceDetected:
        return 'No Face Detected';
      case FaceValidationType.faceTooSmall:
        return 'Face Too Far Away';
      case FaceValidationType.faceTooTilted:
        return 'Face Not Centered';
      case FaceValidationType.multipleFaces:
        return 'Multiple Faces Detected';
      case FaceValidationType.poorLighting:
        return 'Poor Lighting';
      default:
        return 'Detection Error';
    }
  }

  String _getHelpfulTip() {
    switch (validationResult.validationType) {
      case FaceValidationType.noFaceDetected:
        return 'Make sure to take a clear selfie with your face visible. Avoid uploading screenshots or non-face images.';
      case FaceValidationType.faceTooSmall:
        return 'Hold your phone closer to your face, about arm\'s length away for best results.';
      case FaceValidationType.faceTooTilted:
        return 'Look directly at the camera and keep your head straight for accurate analysis.';
      case FaceValidationType.multipleFaces:
        return 'Please take a photo with only your face visible for personalized analysis.';
      case FaceValidationType.poorLighting:
        return 'Find a well-lit area with natural light for the most accurate skin analysis.';
      default:
        return 'Please try taking a new photo with good lighting and your face clearly visible.';
    }
  }
}

/// Simple dialog to show face detection error
class FaceValidationDialog extends StatelessWidget {
  final FaceValidationResult validationResult;

  const FaceValidationDialog({super.key, required this.validationResult});

  static Future<void> show(BuildContext context, FaceValidationResult result) {
    return showDialog(
      context: context,
      builder: (context) => FaceValidationDialog(validationResult: result),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.face_retouching_off,
            size: 60,
            color: Colors.red[400],
          ),
          const SizedBox(height: 16),
          Text(
            'No Face Detected',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
          ),
          const SizedBox(height: 8),
          Text(
            validationResult.message,
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey[600]),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Try Again'),
        ),
      ],
    );
  }
}
