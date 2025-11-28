"""Face Detection Service - Validate face presence in images.

This module provides face detection capabilities using OpenCV's
Haar Cascade classifier for validating that uploaded images
contain a human face before skin analysis.

Features:
- Fast face detection using Haar Cascades
- Support for multiple image formats
- Configurable detection parameters
- Async-compatible interface

Author: AI Engineering Team
Version: 1.0.0
Last Updated: November 28, 2025
"""

import cv2
import numpy as np
import logging
from typing import Optional, Tuple
import io

logger = logging.getLogger(__name__)

# Load Haar Cascade classifier for face detection
# This is a pre-trained model included with OpenCV
try:
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    FACE_CASCADE_LOADED = True
except Exception as e:
    logger.error(f"Failed to load face cascade classifier: {e}")
    FACE_CASCADE_LOADED = False
    face_cascade = None


async def detect_face_in_image(
    image_data: bytes,
    min_face_size: Tuple[int, int] = (30, 30),
    scale_factor: float = 1.1,
    min_neighbors: int = 5
) -> bool:
    """
    Detect if a human face is present in the image.
    
    Args:
        image_data: Raw image bytes (JPEG, PNG)
        min_face_size: Minimum face size to detect (width, height)
        scale_factor: Scale factor for the detection algorithm
        min_neighbors: Minimum neighbors for detection confidence
    
    Returns:
        True if at least one face is detected, False otherwise
    
    Raises:
        ValueError: If image data is invalid or cannot be processed
    """
    if not FACE_CASCADE_LOADED:
        logger.warning("Face cascade not loaded, skipping face detection")
        # Return True to allow processing if face detection is unavailable
        # In production, you might want to return False or raise an exception
        return True
    
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        
        # Decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            logger.error("Failed to decode image data")
            return False
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the image
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_face_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        num_faces = len(faces)
        logger.info(f"Face detection result: {num_faces} face(s) found")
        
        # Return True if at least one face is detected
        return num_faces > 0
        
    except cv2.error as e:
        logger.error(f"OpenCV error during face detection: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during face detection: {e}")
        return False


def get_face_detection_info(image_data: bytes) -> dict:
    """
    Get detailed face detection information.
    
    Args:
        image_data: Raw image bytes
    
    Returns:
        Dictionary with face detection details:
        - detected: bool - whether faces were found
        - count: int - number of faces detected
        - faces: list - bounding boxes for each face
        - image_size: tuple - original image dimensions
    """
    result = {
        "detected": False,
        "count": 0,
        "faces": [],
        "image_size": (0, 0)
    }
    
    if not FACE_CASCADE_LOADED:
        result["error"] = "Face detection not available"
        return result
    
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            result["error"] = "Invalid image data"
            return result
        
        result["image_size"] = (img.shape[1], img.shape[0])  # width, height
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        result["count"] = len(faces)
        result["detected"] = len(faces) > 0
        result["faces"] = [
            {
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h)
            }
            for (x, y, w, h) in faces
        ]
        
    except Exception as e:
        result["error"] = str(e)
    
    return result