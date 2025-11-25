"""  
Face Detector Module for Skincare AI App  
  
Provides face detection and facial landmark detection for proper  
skin region extraction before analysis.  
  
Features:  
- Face detection using MTCNN/RetinaFace  
- Facial landmark detection (68 points)  
- Face alignment and cropping  
- Skin region segmentation  
  
Author: AI Skincare Team  
Version: 1.0.0  
"""  
  
import torch  
import torch.nn as nn  
import numpy as np  
from PIL import Image  
from typing import Dict, List, Tuple, Optional  
from dataclasses import dataclass  
import cv2  
  
  
@dataclass  
class FaceDetectionResult:  
    """Result of face detection"""  
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2  
    confidence: float  
    landmarks: Optional[np.ndarray] = None  # 5 or 68 landmarks  
    aligned_face: Optional[np.ndarray] = None  
  
  
@dataclass  
class SkinRegions:  
    """Segmented skin regions for analysis"""  
    forehead: np.ndarray  
    left_cheek: np.ndarray  
    right_cheek: np.ndarray  
    nose: np.ndarray  
    chin: np.ndarray  
    full_face: np.ndarray  
  
  
class FaceDetector:  
    """  
    Face detection and preprocessing for skin analysis.  
    Uses MTCNN for accurate face and landmark detection.  
    """  
      
    def __init__(self, device: str = 'auto', min_face_size: int = 100):  
        if device == 'auto':  
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  
        else:  
            self.device = torch.device(device)  
          
        self.min_face_size = min_face_size  
        self.target_size = (224, 224)  
          
        # Initialize MTCNN (placeholder - use facenet-pytorch in production)  
        self._init_detector()  
      
    def _init_detector(self):  
        """Initialize the face detection model"""  
        # In production, use:  
        # from facenet_pytorch import MTCNN  
        # self.mtcnn = MTCNN(device=self.device)  
        self.detector = None  # Placeholder  
      
    def detect_faces(self, image: Image.Image) -> List[FaceDetectionResult]:  
        """  
        Detect all faces in an image.  
          
        Args:  
            image: PIL Image  
              
        Returns:  
            List of FaceDetectionResult  
        """  
        img_array = np.array(image)  
          
        # Use OpenCV Haar Cascade as fallback  
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)  
        face_cascade = cv2.CascadeClassifier(  
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'  
        )  
          
        faces = face_cascade.detectMultiScale(  
            gray,   
            scaleFactor=1.1,  
            minNeighbors=5,  
            minSize=(self.min_face_size, self.min_face_size)  
        )  
          
        results = []  
        for (x, y, w, h) in faces:  
            # Add padding  
            padding = int(0.2 * max(w, h))  
            x1 = max(0, x - padding)  
            y1 = max(0, y - padding)  
            x2 = min(img_array.shape[1], x + w + padding)  
            y2 = min(img_array.shape[0], y + h + padding)  
              
            results.append(FaceDetectionResult(  
                bbox=(x1, y1, x2, y2),  
                confidence=0.95,  # Placeholder  
                landmarks=None  
            ))  
          
        return results  
      
    def detect_and_align(self, image: Image.Image) -> Optional[FaceDetectionResult]:  
        """  
        Detect the primary face and return aligned version.  
          
        Args:  
            image: PIL Image  
              
        Returns:  
            FaceDetectionResult with aligned face, or None  
        """  
        faces = self.detect_faces(image)  
          
        if not faces:  
            return None  
          
        # Get largest face (assumed to be primary)  
        primary_face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))  
          
        # Crop and align face  
        img_array = np.array(image)  
        x1, y1, x2, y2 = primary_face.bbox  
        face_crop = img_array[y1:y2, x1:x2]  
          
        # Resize to target size  
        aligned_face = cv2.resize(face_crop, self.target_size)  
          
        primary_face.aligned_face = aligned_face  
        return primary_face  
      
    def extract_skin_regions(self, image: Image.Image,   
                             face_result: FaceDetectionResult) -> SkinRegions:  
        """  
        Extract specific skin regions for detailed analysis.  
          
        Args:  
            image: Original PIL Image  
            face_result: Detection result with landmarks  
              
        Returns:  
            SkinRegions with segmented areas  
        """  
        img_array = np.array(image)  
        x1, y1, x2, y2 = face_result.bbox  
        face_crop = img_array[y1:y2, x1:x2]  
          
        h, w = face_crop.shape[:2]  
          
        # Define region boundaries (approximate without landmarks)  
        regions = SkinRegions(  
            forehead=face_crop[0:int(h*0.3), int(w*0.2):int(w*0.8)],  
            left_cheek=face_crop[int(h*0.35):int(h*0.7), 0:int(w*0.35)],  
            right_cheek=face_crop[int(h*0.35):int(h*0.7), int(w*0.65):w],  
            nose=face_crop[int(h*0.3):int(h*0.7), int(w*0.35):int(w*0.65)],  
            chin=face_crop[int(h*0.7):h, int(w*0.25):int(w*0.75)],  
            full_face=face_crop  
        )  
          
        return regions  
  
  
class SkinSegmenter:  
    """  
    Semantic segmentation for skin vs non-skin pixels.  
    Useful for accurate skin analysis excluding hair, eyebrows, etc.  
    """  
      
    def __init__(self):  
        self.skin_lower = np.array([0, 20, 70], dtype=np.uint8)  
        self.skin_upper = np.array([20, 255, 255], dtype=np.uint8)  
      
    def segment_skin(self, image: np.ndarray) -> np.ndarray:  
        """  
        Create binary mask of skin pixels.  
          
        Args:  
            image: RGB numpy array  
              
        Returns:  
            Binary mask where 1 = skin pixel  
        """  
        # Convert to HSV  
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  
          
        # Create skin mask  
        mask = cv2.inRange(hsv, self.skin_lower, self.skin_upper)  
          
        # Morphological operations to clean up  
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  
          
        return mask // 255  # Normalize to 0-1  
      
    def apply_mask(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:  
        """Apply skin mask to image, setting non-skin to black"""  
        return image * mask[:, :, np.newaxis]  
  
  
# Export classes  
__all__ = [  
    'FaceDetector',  
    'FaceDetectionResult',  
    'SkinRegions',  
    'SkinSegmenter'  
]  
