/**
 * Face Detection Web Service using face-api.js
 * Provides web-compatible face detection for skincare analysis
 * 
 * This file bridges the Flutter/Dart code with face-api.js
 */

// Global state
let faceApiLoaded = false;
let modelsLoaded = false;

// Model URLs - using jsdelivr CDN for face-api.js models
const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.12/model';

/**
 * Initialize face-api.js and load required models
 */
async function initializeFaceApi() {
  if (modelsLoaded) {
    console.log('Face API models already loaded');
    return true;
  }

  try {
    console.log('Loading face-api.js models...');
    
    // Load required models for face detection and landmarks
    await Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
      faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
      faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL)
    ]);
    
    modelsLoaded = true;
    console.log('Face API models loaded successfully');
    return true;
  } catch (error) {
    console.error('Failed to load face-api.js models:', error);
    return false;
  }
}

/**
 * Detect faces in an image from base64 data
 * @param {string} base64Image - Base64 encoded image data
 * @returns {Promise<Object>} - Detection result with faces array or error
 */
async function detectFacesFromBase64(base64Image) {
  if (!modelsLoaded) {
    const initialized = await initializeFaceApi();
    if (!initialized) {
      return {
        success: false,
        errorMessage: 'Face detection models failed to load. Please refresh the page.',
        faces: []
      };
    }
  }

  try {
    // Create image element from base64
    const img = await createImageFromBase64(base64Image);
    
    // Detect faces with landmarks and expressions
    const detections = await faceapi
      .detectAllFaces(img, new faceapi.TinyFaceDetectorOptions({
        inputSize: 416,
        scoreThreshold: 0.5
      }))
      .withFaceLandmarks()
      .withFaceExpressions();
    
    if (!detections || detections.length === 0) {
      return {
        success: false,
        errorMessage: 'No face detected! Please upload a clear photo of your face for skin analysis.',
        faces: []
      };
    }

    // Convert detections to our format
    const faces = detections.map(detection => {
      const box = detection.detection.box;
      const landmarks = detection.landmarks;
      
      return {
        boundingBox: {
          x: box.x,
          y: box.y,
          width: box.width,
          height: box.height
        },
        landmarks: extractLandmarks(landmarks),
        expressions: detection.expressions,
        confidence: detection.detection.score
      };
    });

    console.log(`Detected ${faces.length} face(s)`);
    
    return {
      success: true,
      errorMessage: null,
      faces: faces
    };

  } catch (error) {
    console.error('Face detection error:', error);
    return {
      success: false,
      errorMessage: 'Failed to analyze image. Please try again with a different photo.',
      faces: []
    };
  }
}

/**
 * Create an image element from base64 string
 */
function createImageFromBase64(base64) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    
    img.onload = () => resolve(img);
    img.onerror = (err) => reject(new Error('Failed to load image'));
    
    // Add data URL prefix if not present
    if (!base64.startsWith('data:')) {
      base64 = 'data:image/jpeg;base64,' + base64;
    }
    img.src = base64;
  });
}

/**
 * Extract facial landmarks in our format
 */
function extractLandmarks(landmarks) {
  if (!landmarks) return {};
  
  const positions = landmarks.positions;
  
  return {
    leftEye: averagePoints(landmarks.getLeftEye()),
    rightEye: averagePoints(landmarks.getRightEye()),
    nose: averagePoints(landmarks.getNose()),
    mouth: averagePoints(landmarks.getMouth()),
    jawOutline: landmarks.getJawOutline().map(p => ({ x: p.x, y: p.y })),
    leftCheek: positions[1] ? { x: positions[1].x, y: positions[1].y } : null,
    rightCheek: positions[15] ? { x: positions[15].x, y: positions[15].y } : null
  };
}

/**
 * Calculate average point from array of points
 */
function averagePoints(points) {
  if (!points || points.length === 0) return null;
  
  const sum = points.reduce((acc, p) => ({
    x: acc.x + p.x,
    y: acc.y + p.y
  }), { x: 0, y: 0 });
  
  return {
    x: sum.x / points.length,
    y: sum.y / points.length
  };
}

/**
 * Validate if the detected face is suitable for skin analysis
 */
function validateFaceForAnalysis(face) {
  const box = face.boundingBox;
  
  // Check minimum face size
  if (box.width < 100 || box.height < 100) {
    return {
      isValid: false,
      message: 'Please move closer to the camera for better analysis.',
      validationType: 'faceTooSmall'
    };
  }
  
  // Check confidence score
  if (face.confidence < 0.7) {
    return {
      isValid: false,
      message: 'Face not clearly visible. Please ensure good lighting.',
      validationType: 'lowConfidence'
    };
  }
  
  return {
    isValid: true,
    message: 'Face detected successfully!',
    validationType: 'valid'
  };
}

/**
 * Get skin analysis zones from detected face
 */
function getSkinAnalysisZones(face) {
  const box = face.boundingBox;
  
  return {
    forehead: {
      x: box.x + box.width * 0.2,
      y: box.y,
      width: box.width * 0.6,
      height: box.height * 0.2
    },
    leftCheek: {
      x: box.x,
      y: box.y + box.height * 0.3,
      width: box.width * 0.3,
      height: box.height * 0.3
    },
    rightCheek: {
      x: box.x + box.width * 0.7,
      y: box.y + box.height * 0.3,
      width: box.width * 0.3,
      height: box.height * 0.3
    },
    nose: {
      x: box.x + box.width * 0.35,
      y: box.y + box.height * 0.35,
      width: box.width * 0.3,
      height: box.height * 0.25
    },
    chin: {
      x: box.x + box.width * 0.25,
      y: box.y + box.height * 0.75,
      width: box.width * 0.5,
      height: box.height * 0.2
    }
  };
}

// Expose functions to window for Dart interop
window.FaceApiWeb = {
  initialize: initializeFaceApi,
  detectFaces: detectFacesFromBase64,
  validateFace: validateFaceForAnalysis,
  getSkinZones: getSkinAnalysisZones,
  isLoaded: () => modelsLoaded
};

// Auto-initialize when script loads
if (typeof faceapi !== 'undefined') {
  faceApiLoaded = true;
  console.log('face-api.js library detected');
}
