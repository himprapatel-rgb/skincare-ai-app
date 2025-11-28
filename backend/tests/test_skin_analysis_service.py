"""Tests for Skin Analysis Service

This module contains comprehensive tests for the skin analysis service,
including unit tests and integration tests.

Author: AI Engineering Team
Version: 1.0.0
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.skin_analysis_service import (
    SkinAnalysisService,
    SkinAnalysisResult,
    SkinMetrics,
    SkinConcern,
    skin_analysis_service
)


class TestSkinAnalysisService:
    """Test suite for SkinAnalysisService."""
    
    @pytest.fixture
    def service(self):
        """Create a fresh service instance for each test."""
        return SkinAnalysisService()
    
    @pytest.fixture
    def mock_rapidapi_response(self):
        """Mock successful RapidAPI response."""
        return {
            "acne": {"score": 35, "confidence": 0.85},
            "wrinkles": {"score": 20, "confidence": 0.90},
            "dark_spots": {"score": 15, "confidence": 0.88},
            "dark_circles": {"score": 40, "confidence": 0.82},
            "pores": {"score": 30, "confidence": 0.87},
            "hydration": {"score": 65},
            "oiliness": {"score": 45},
            "texture": {"score": 70},
            "elasticity": {"score": 75},
            "evenness": {"score": 72},
            "skin_type": "combination",
            "skin_age": 28,
            "confidence": 0.88,
            "image_quality": 0.92
        }
    
    def test_service_initialization(self, service):
        """Test service initializes correctly."""
        assert service is not None
        assert service.timeout == 30.0
        assert len(service.concern_recommendations) > 0
    
    def test_score_to_severity_none(self, service):
        """Test severity conversion for low scores."""
        assert service._score_to_severity(0) == "none"
        assert service._score_to_severity(19) == "none"
    
    def test_score_to_severity_mild(self, service):
        """Test severity conversion for mild scores."""
        assert service._score_to_severity(20) == "mild"
        assert service._score_to_severity(39) == "mild"
    
    def test_score_to_severity_moderate(self, service):
        """Test severity conversion for moderate scores."""
        assert service._score_to_severity(40) == "moderate"
        assert service._score_to_severity(59) == "moderate"
    
    def test_score_to_severity_severe(self, service):
        """Test severity conversion for severe scores."""
        assert service._score_to_severity(60) == "severe"
        assert service._score_to_severity(79) == "severe"
    
    def test_score_to_severity_very_severe(self, service):
        """Test severity conversion for very severe scores."""
        assert service._score_to_severity(80) == "very_severe"
        assert service._score_to_severity(100) == "very_severe"
    
    def test_calculate_overall_score(self, service):
        """Test overall score calculation."""
        metrics = SkinMetrics(
            hydration_score=70,
            oiliness_score=50,
            texture_score=75,
            elasticity_score=80,
            pore_size_score=65,
            skin_tone_evenness=72
        )
        concerns = []
        
        score = service._calculate_overall_score(concerns, metrics)
        assert 0 <= score <= 100
        assert score > 60  # Should be relatively high with no concerns
    
    def test_calculate_overall_score_with_concerns(self, service):
        """Test overall score with skin concerns."""
        metrics = SkinMetrics()
        concerns = [
            SkinConcern(
                concern_type="acne",
                severity="moderate",
                confidence=0.85
            ),
            SkinConcern(
                concern_type="wrinkles",
                severity="mild",
                confidence=0.80
            )
        ]
        
        score = service._calculate_overall_score(concerns, metrics)
        # Score should be reduced due to concerns
        assert score < 50  # Default metrics - penalties
    
    def test_generate_recommendations_basic(self, service):
        """Test basic recommendations generation."""
        recommendations = service._generate_recommendations([])
        
        assert len(recommendations) >= 3
        assert any("SPF" in r for r in recommendations)
        assert any("cleanser" in r.lower() for r in recommendations)
    
    def test_generate_recommendations_with_concerns(self, service):
        """Test recommendations with specific concerns."""
        concerns = [
            SkinConcern(
                concern_type="acne",
                severity="moderate",
                confidence=0.85
            )
        ]
        
        recommendations = service._generate_recommendations(concerns)
        assert len(recommendations) > 3
    
    def test_get_fallback_result(self, service):
        """Test fallback result structure."""
        result = service._get_fallback_result()
        
        assert isinstance(result, SkinAnalysisResult)
        assert result.overall_score == 50.0
        assert result.skin_type == "unknown"
        assert result.confidence_score == 0.0
    
    @pytest.mark.asyncio
    async def test_analyze_locally(self, service):
        """Test local analysis returns valid result."""
        result = await service._analyze_locally(
            image_url="https://example.com/face.jpg"
        )
        
        assert isinstance(result, SkinAnalysisResult)
        assert 0 <= result.overall_score <= 100
        assert result.skin_type in ["oily", "dry", "combination", "normal", "sensitive"]
        assert result.confidence_score > 0
    
    def test_parse_rapidapi_response(self, service, mock_rapidapi_response):
        """Test parsing of RapidAPI response."""
        result = service._parse_rapidapi_response(mock_rapidapi_response)
        
        assert isinstance(result, SkinAnalysisResult)
        assert result.skin_type == "combination"
        assert result.skin_age == 28
        assert len(result.concerns) > 0
        assert result.metrics.hydration_score == 65
    
    @pytest.mark.asyncio
    async def test_analyze_skin_without_api_key(self, service):
        """Test analysis falls back to local when no API key."""
        service.rapidapi_key = ""
        
        result = await service.analyze_skin(
            image_url="https://example.com/face.jpg"
        )
        
        assert isinstance(result, SkinAnalysisResult)
        assert result.confidence_score == 0.6  # Local analysis confidence


class TestSkinAnalysisModels:
    """Test suite for Pydantic models."""
    
    def test_skin_metrics_defaults(self):
        """Test SkinMetrics default values."""
        metrics = SkinMetrics()
        
        assert metrics.hydration_score == 50.0
        assert metrics.oiliness_score == 50.0
        assert metrics.texture_score == 50.0
    
    def test_skin_concern_validation(self):
        """Test SkinConcern validation."""
        concern = SkinConcern(
            concern_type="acne",
            severity="moderate",
            confidence=0.85
        )
        
        assert concern.concern_type == "acne"
        assert 0 <= concern.confidence <= 1
    
    def test_skin_analysis_result_structure(self):
        """Test SkinAnalysisResult structure."""
        result = SkinAnalysisResult(
            overall_score=75.5,
            skin_type="combination",
            concerns=[],
            metrics=SkinMetrics(),
            recommendations=[],
            analysis_timestamp=datetime.utcnow(),
            confidence_score=0.9,
            image_quality_score=0.85
        )
        
        assert result.overall_score == 75.5
        assert result.skin_type == "combination"


class TestSkinAnalysisSingleton:
    """Test the singleton instance."""
    
    def test_singleton_exists(self):
        """Test singleton instance is available."""
        assert skin_analysis_service is not None
        assert isinstance(skin_analysis_service, SkinAnalysisService)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
