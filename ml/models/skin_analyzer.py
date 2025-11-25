"""  
Skin Analyzer - Core AI Module for Skincare Analysis  
  
This module provides the main skin analysis functionality using deep learning  
models for detecting skin conditions, concerns, and providing personalized  
recommendations.  
  
Based on research from top 20 skincare AI apps including:  
- SkinVision (3-indicator camera quality system)  
- Haut.AI (150+ biomarkers)  
- Skin Bliss (ingredient compatibility)  
- Cureskin (dermatologist integration)  
  
Author: AI Skincare Team  
Version: 1.0.0  
Date: November 2025  
"""  
  
import torch  
import torch.nn as nn  
import torchvision.transforms as transforms  
import torchvision.models as models  
from PIL import Image  
import numpy as np  
from typing import Dict, List, Tuple, Optional  
from dataclasses import dataclass  
from enum import Enum  
import json  
  
  
class SkinConcern(Enum):  
    """Enumeration of detectable skin concerns"""  
    ACNE = "acne"  
    WRINKLES = "wrinkles"  
    DARK_SPOTS = "dark_spots"  
    REDNESS = "redness"  
    DRYNESS = "dryness"  
    OILINESS = "oiliness"  
    LARGE_PORES = "large_pores"  
    UNEVEN_TEXTURE = "uneven_texture"  
    DARK_CIRCLES = "dark_circles"  
    HYPERPIGMENTATION = "hyperpigmentation"  
    DEHYDRATION = "dehydration"  
    SENSITIVITY = "sensitivity"  
  
  
class SkinType(Enum):  
    """Skin type classification"""  
    DRY = "dry"  
    OILY = "oily"  
    COMBINATION = "combination"  
    NORMAL = "normal"  
    SENSITIVE = "sensitive"  
  
  
class RiskLevel(Enum):  
    """Risk level for detected conditions"""  
    LOW = "low"  
    MODERATE = "moderate"  
    HIGH = "high"  
    CRITICAL = "critical"  
  
  
@dataclass  
class SkinAnalysisResult:  
    """Data class for skin analysis results"""  
    overall_score: float  # 0-100  
    skin_type: SkinType  
    concerns: Dict[SkinConcern, float]  # concern -> confidence  
    risk_level: RiskLevel  
    recommendations: List[str]  
    biomarkers: Dict[str, float]  
    skin_age: Optional[int] = None  
    hydration_level: Optional[float] = None  
    texture_score: Optional[float] = None  
  
  
class ImageQualityChecker:  
    """  
    Validates image quality before analysis.  
    Based on SkinVision's 3-indicator system.  
    """  
      
    def __init__(self):  
        self.min_resolution = (640, 480)  
        self.min_brightness = 40  
        self.max_brightness = 220  
        self.min_sharpness = 100  
      
    def check_quality(self, image: Image.Image) -> Dict[str, bool]:  
        """  
        Check image quality with 3 indicators:  
        - In Focus: Image sharpness  
        - Detected: Face/skin region found  
        - Clear: Proper lighting  
        """  
        img_array = np.array(image)  
          
        # Check resolution  
        resolution_ok = (  
            image.size[0] >= self.min_resolution[0] and  
            image.size[1] >= self.min_resolution[1]  
        )  
          
        # Check brightness (lighting)  
        brightness = np.mean(img_array)  
        lighting_ok = self.min_brightness <= brightness <= self.max_brightness  
          
        # Check sharpness using Laplacian variance  
        gray = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array  
        laplacian_var = self._calculate_laplacian_variance(gray)  
        sharpness_ok = laplacian_var >= self.min_sharpness  
          
        return {  
            "in_focus": sharpness_ok,  
            "detected": resolution_ok,  # Simplified; use face detection in production  
            "clear": lighting_ok,  
            "overall_quality": all([sharpness_ok, resolution_ok, lighting_ok])  
        }  
      
    def _calculate_laplacian_variance(self, gray_image: np.ndarray) -> float:  
        """Calculate Laplacian variance for sharpness detection"""  
        from scipy import ndimage  
        laplacian = ndimage.laplace(gray_image)  
        return np.var(laplacian)  


class SkinAnalyzerModel(nn.Module):
    """
    Deep Learning model for skin analysis.
    Uses transfer learning with EfficientNet backbone.
    Analyzes 150+ biomarkers based on Haut.AI research.
    """
    
    def __init__(self, num_concerns: int = 12, num_biomarkers: int = 150):
        super().__init__()
        
        # Load pretrained EfficientNet backbone
        self.backbone = models.efficientnet_b0(pretrained=True)
        
        # Get the number of features from backbone
        num_features = self.backbone.classifier[1].in_features
        
        # Remove original classifier
        self.backbone.classifier = nn.Identity()
        
        # Skin type classifier (5 types)
        self.skin_type_head = nn.Sequential(
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 5)
        )
        
        # Concern detector (multi-label)
        self.concern_head = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_concerns),
            nn.Sigmoid()
        )
        
        # Biomarker regressor
        self.biomarker_head = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, num_biomarkers),
            nn.Sigmoid()  # Normalize to 0-1
        )
        
        # Overall score regressor
        self.score_head = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()  # Score 0-1, multiply by 100
        )
        
        # Skin age estimator
        self.age_head = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
    
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Forward pass returning all predictions"""
        features = self.backbone(x)
        
        return {
            'skin_type': self.skin_type_head(features),
            'concerns': self.concern_head(features),
            'biomarkers': self.biomarker_head(features),
            'overall_score': self.score_head(features) * 100,
            'skin_age': self.age_head(features)
        }


class SkinAnalyzer:
    """
    Main skin analysis class that orchestrates the analysis pipeline.
    
    Features:
    - Image quality validation (SkinVision-inspired)
    - Deep learning skin analysis
    - Concern detection and severity scoring
    - Personalized recommendations
    - Risk level assessment
    """
    
    def __init__(self, model_path: Optional[str] = None, device: str = 'auto'):
        # Set device
        if device == 'auto':
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        # Initialize components
        self.quality_checker = ImageQualityChecker()
        self.model = SkinAnalyzerModel().to(self.device)
        
        # Load trained weights if provided
        if model_path:
            self.load_model(model_path)
        
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Concern labels mapping
        self.concern_labels = list(SkinConcern)
        
        # Biomarker names (simplified list)
        self.biomarker_names = self._get_biomarker_names()
    
    def _get_biomarker_names(self) -> List[str]:
        """Get list of 150+ biomarker names based on Haut.AI research"""
        return [
            'hydration_level', 'oil_production', 'pore_size', 'skin_texture',
            'fine_lines', 'deep_wrinkles', 'elasticity', 'firmness',
            'pigmentation_uniformity', 'melanin_index', 'hemoglobin_index',
            'redness_intensity', 'acne_severity', 'blackheads_count',
            'whiteheads_count', 'skin_brightness', 'radiance_score',
            'dark_circle_intensity', 'eye_puffiness', 'skin_thickness',
            # ... extend to 150 biomarkers
        ]
    
    def load_model(self, model_path: str):
        """Load trained model weights"""
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()
    
    def analyze(self, image: Image.Image, validate_quality: bool = True) -> SkinAnalysisResult:
        """
        Perform comprehensive skin analysis on an image.
        
        Args:
            image: PIL Image of the face/skin area
            validate_quality: Whether to check image quality first
        
        Returns:
            SkinAnalysisResult with all analysis data
        """
        # Step 1: Quality Check
        if validate_quality:
            quality = self.quality_checker.check_quality(image)
            if not quality['overall_quality']:
                raise ValueError(f"Image quality check failed: {quality}")
        
        # Step 2: Preprocess image
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Step 3: Run inference
        with torch.no_grad():
            outputs = self.model(input_tensor)
        
        # Step 4: Process results
        return self._process_outputs(outputs)
    
    def _process_outputs(self, outputs: Dict[str, torch.Tensor]) -> SkinAnalysisResult:
        """Process model outputs into structured result"""
        
        # Get skin type
        skin_type_idx = outputs['skin_type'].argmax(dim=1).item()
        skin_type = list(SkinType)[skin_type_idx]
        
        # Get concerns with confidence scores
        concern_scores = outputs['concerns'].squeeze().cpu().numpy()
        concerns = {
            self.concern_labels[i]: float(score)
            for i, score in enumerate(concern_scores)
            if score > 0.3  # Threshold for detection
        }
        
        # Get biomarkers
        biomarker_values = outputs['biomarkers'].squeeze().cpu().numpy()
        biomarkers = {
            name: float(value)
            for name, value in zip(self.biomarker_names[:len(biomarker_values)], biomarker_values)
        }
        
        # Calculate overall score
        overall_score = float(outputs['overall_score'].item())
        
        # Estimate skin age
        skin_age = int(outputs['skin_age'].item())
        
        # Determine risk level based on concerns
        risk_level = self._calculate_risk_level(concerns)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(skin_type, concerns, biomarkers)
        
        return SkinAnalysisResult(
            overall_score=overall_score,
            skin_type=skin_type,
            concerns=concerns,
            risk_level=risk_level,
            recommendations=recommendations,
            biomarkers=biomarkers,
            skin_age=skin_age,
            hydration_level=biomarkers.get('hydration_level'),
            texture_score=biomarkers.get('skin_texture')
        )
    
    def _calculate_risk_level(self, concerns: Dict[SkinConcern, float]) -> RiskLevel:
        """Calculate risk level based on detected concerns"""
        if not concerns:
            return RiskLevel.LOW
        
        max_confidence = max(concerns.values())
        num_concerns = len(concerns)
        
        if max_confidence > 0.9 or num_concerns > 5:
            return RiskLevel.HIGH
        elif max_confidence > 0.7 or num_concerns > 3:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW
    
    def _generate_recommendations(self, skin_type: SkinType, 
                                   concerns: Dict[SkinConcern, float],
                                   biomarkers: Dict[str, float]) -> List[str]:
        """Generate personalized skincare recommendations"""
        recommendations = []
        
        # Skin type specific recommendations
        skin_type_recs = {
            SkinType.DRY: "Use a rich, hydrating moisturizer with hyaluronic acid.",
            SkinType.OILY: "Choose oil-free, non-comedogenic products with niacinamide.",
            SkinType.COMBINATION: "Use lightweight moisturizer, focus heavier products on dry areas.",
            SkinType.NORMAL: "Maintain your routine with balanced, gentle products.",
            SkinType.SENSITIVE: "Use fragrance-free, hypoallergenic products with ceramides."
        }
        recommendations.append(skin_type_recs.get(skin_type, ""))
        
        # Concern-specific recommendations
        concern_recs = {
            SkinConcern.ACNE: "Include salicylic acid or benzoyl peroxide in your routine.",
            SkinConcern.WRINKLES: "Apply retinol at night and use SPF 50+ daily.",
            SkinConcern.DARK_SPOTS: "Use vitamin C serum in the morning.",
            SkinConcern.DRYNESS: "Add a hydrating serum with hyaluronic acid.",
            SkinConcern.REDNESS: "Use calming ingredients like centella asiatica.",
            SkinConcern.LARGE_PORES: "Try niacinamide to minimize pore appearance."
        }
        
        for concern in concerns:
            if concern in concern_recs:
                recommendations.append(concern_recs[concern])
        
        return recommendations[:5]  # Limit to top 5 recommendations


# Export main classes
__all__ = [
    'SkinAnalyzer',
    'SkinAnalyzerModel',
    'SkinAnalysisResult',
    'SkinConcern',
    'SkinType',
    'RiskLevel',
    'ImageQualityChecker'
]
