"""
Ingredient Scanning & Analysis API Routes

This module implements comprehensive ingredient analysis and product safety checking including:
- Barcode scanning and product lookup
- INCI ingredient decoding and analysis
- Safety ratings and allergen detection
- Personalized warnings based on skin type
- Product compatibility checking
- Ingredient education and alternatives

Based on SRS FR-3.5: Ingredient Scanner Requirements
- Scan product barcodes to retrieve ingredient lists
- Analyze ingredients for safety and potential irritants
- Detect allergens and harmful chemicals
- Provide personalized warnings based on user's skin concerns
- Suggest safer product alternatives
- Educational content about each ingredient

Inspired by top apps researched:
- Yuka: Barcode scanning & safety ratings
- INCI Decoder: Comprehensive ingredient analysis
- Think Dirty: Hazard scoring system
- CosDNA: Detailed ingredient database

Author: AI Skincare App Team
Version: 1.0
Created: 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional, Dict
import logging

from app.core.database import get_db
from app.models.user import User
from app.api.v1.routes.auth import get_current_user

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredient Scanner"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)


# Request/Response Models
from pydantic import BaseModel, Field, validator


class IngredientDetail(BaseModel):
    """Detailed information about a single ingredient"""
    inci_name: str = Field(..., description="INCI (International Nomenclature) name")
    common_name: Optional[str] = Field(None, description="Common/marketing name")
    function: str = Field(..., description="Primary function: moisturizer, preservative, etc.")
    safety_rating: int = Field(..., ge=1, le=5, description="Safety rating 1-5 (1=best, 5=worst)")
    comedogenic_rating: int = Field(..., ge=0, le=5, description="Pore-clogging potential 0-5")
    is_allergen: bool = False
    is_irritant: bool = False
    is_fragrance: bool = False
    warnings: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    concerns_for: List[str] = Field(default_factory=list, description="Skin types to be cautious")
    
    class Config:
        json_schema_extra = {
            "example": {
                "inci_name": "Sodium Hyaluronate",
                "common_name": "Hyaluronic Acid",
                "function": "Humectant/Moisturizer",
                "safety_rating": 1,
                "comedogenic_rating": 0,
                "is_allergen": False,
                "is_irritant": False,
                "is_fragrance": False,
                "warnings": [],
                "benefits": ["Intense hydration", "Plumping effect", "Suitable for all skin types"],
                "concerns_for": []
            }
        }


class ProductAnalysis(BaseModel):
    """Complete product analysis with all ingredients"""
    product_id: Optional[str] = None
    product_name: str
    brand: Optional[str] = None
    barcode: Optional[str] = None
    category: Optional[str] = None
    overall_safety_score: float = Field(..., ge=0.0, le=100.0)
    hazard_level: str = Field(..., description="low, moderate, high")
    ingredients: List[IngredientDetail]
    total_ingredients: int
    flagged_ingredients: List[str] = Field(default_factory=list)
    personalized_warnings: List[str] = Field(default_factory=list)
    is_compatible: bool = True
    alternatives: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "PROD123",
                "product_name": "Gentle Hydrating Cleanser",
                "brand": "CeraVe",
                "barcode": "3606000437128",
                "category": "Cleanser",
                "overall_safety_score": 85.5,
                "hazard_level": "low",
                "ingredients": [],
                "total_ingredients": 15,
                "flagged_ingredients": [],
                "personalized_warnings": [],
                "is_compatible": True,
                "alternatives": []
            }
        }


# Helper Functions

def analyze_ingredient_safety(inci_name: str, user_skin_concerns: List[str] = None) -> IngredientDetail:
    """
    Analyze a single ingredient for safety and compatibility.
    
    Args:
        inci_name: INCI name of ingredient
        user_skin_concerns: User's specific skin concerns for personalized warnings
    
    Returns:
        IngredientDetail with complete analysis
    
    Note:
        In production, this would query a comprehensive ingredient database.
        Current implementation uses mock data for demonstration.
    """
    # TODO: Integrate with real ingredient database (CosDNA, EWG, etc.)
    
    # Mock ingredient database
    ingredient_db = {
        "sodium hyaluronate": {
            "common_name": "Hyaluronic Acid",
            "function": "Humectant/Moisturizer",
            "safety_rating": 1,
            "comedogenic_rating": 0,
            "benefits": ["Intense hydration", "Plumping effect", "Anti-aging"],
            "concerns_for": []
        },
        "alcohol denat": {
            "common_name": "Alcohol",
            "function": "Solvent/Preservative",
            "safety_rating": 3,
            "comedogenic_rating": 0,
            "is_irritant": True,
            "warnings": ["Can be drying", "May irritate sensitive skin"],
            "concerns_for": ["dry_skin", "sensitive_skin"]
        },
        "parfum": {
            "common_name": "Fragrance",
            "function": "Fragrance",
            "safety_rating": 4,
            "comedogenic_rating": 0,
            "is_allergen": True,
            "is_fragrance": True,
            "warnings": ["Common allergen", "May cause irritation"],
            "concerns_for": ["sensitive_skin", "rosacea"]
        }
    }
    
    # Normalize ingredient name
    inci_lower = inci_name.lower()
    
    if inci_lower in ingredient_db:
        ing_data = ingredient_db[inci_lower]
        return IngredientDetail(
            inci_name=inci_name,
            common_name=ing_data.get("common_name"),
            function=ing_data["function"],
            safety_rating=ing_data["safety_rating"],
            comedogenic_rating=ing_data["comedogenic_rating"],
            is_allergen=ing_data.get("is_allergen", False),
            is_irritant=ing_data.get("is_irritant", False),
            is_fragrance=ing_data.get("is_fragrance", False),
            warnings=ing_data.get("warnings", []),
            benefits=ing_data.get("benefits", []),
            concerns_for=ing_data.get("concerns_for", [])
        )
    else:
        # Default for unknown ingredients
        return IngredientDetail(
            inci_name=inci_name,
            common_name=None,
            function="Unknown",
            safety_rating=3,
            comedogenic_rating=0,
            warnings=["Insufficient data available"]
        )


def calculate_safety_score(ingredients: List[IngredientDetail]) -> float:
    """
    Calculate overall product safety score based on ingredient ratings.
    
    Args:
        ingredients: List of analyzed ingredients
    
    Returns:
        Safety score from 0-100 (higher is better)
    """
    if not ingredients:
        return 0.0
    
    # Invert safety ratings (1=best becomes 100, 5=worst becomes 20)
    scores = [(6 - ing.safety_rating) * 20 for ing in ingredients]
    return sum(scores) / len(scores)


# API Endpoints

@router.post(
    "/scan/barcode",
    response_model=ProductAnalysis,
    summary="Scan product barcode",
    description="Scan a product barcode to retrieve and analyze ingredients"
)
async def scan_barcode(
    barcode: str = Query(..., min_length=8, max_length=13, description="Product barcode (EAN/UPC)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ProductAnalysis:
    """
    Scan product barcode and retrieve ingredient analysis.
    
    This endpoint:
    1. Looks up product by barcode in database
    2. Analyzes all ingredients for safety
    3. Provides personalized warnings based on user's skin
    4. Suggests alternatives if needed
    
    Args:
        barcode: Product barcode number
        current_user: Authenticated user
        db: Database session
    
    Returns:
        ProductAnalysis with complete ingredient breakdown
    """
    try:
        logger.info(f"Scanning barcode {barcode} for user {current_user.id}")
        
        # TODO: Query product database by barcode
        # For now, using mock data
        
        # Mock product data
        mock_ingredients = [
            "Water",
            "Sodium Hyaluronate",
            "Glycerin",
            "Niacinamide",
            "Ceramide NP"
        ]
        
        # Analyze each ingredient
        analyzed_ingredients = [
            analyze_ingredient_safety(ing) for ing in mock_ingredients
        ]
        
        # Calculate overall safety
        safety_score = calculate_safety_score(analyzed_ingredients)
        
        # Determine hazard level
        if safety_score >= 80:
            hazard_level = "low"
        elif safety_score >= 60:
            hazard_level = "moderate"
        else:
            hazard_level = "high"
        
        # Identify flagged ingredients
        flagged = [
            ing.inci_name for ing in analyzed_ingredients
            if ing.safety_rating >= 4 or ing.is_allergen
        ]
        
        return ProductAnalysis(
            product_id="MOCK123",
            product_name="CeraVe Hydrating Cleanser",
            brand="CeraVe",
            barcode=barcode,
            category="Cleanser",
            overall_safety_score=round(safety_score, 1),
            hazard_level=hazard_level,
            ingredients=analyzed_ingredients,
            total_ingredients=len(analyzed_ingredients),
            flagged_ingredients=flagged,
            personalized_warnings=[],
            is_compatible=True,
            alternatives=[]
        )
        
    except Exception as e:
        logger.error(f"Error scanning barcode: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to scan barcode"
        )


@router.get(
    "/ingredient/{ingredient_name}",
    response_model=IngredientDetail,
    summary="Look up single ingredient",
    description="Get detailed information about a specific ingredient"
)
async def lookup_ingredient(
    ingredient_name: str,
    current_user: User = Depends(get_current_user)
) -> IngredientDetail:
    """
    Look up detailed information about a specific ingredient.
    
    Provides comprehensive analysis including:
    - INCI and common names
    - Function and purpose
    - Safety and comedogenic ratings
    - Allergen/irritant warnings
    - Benefits and concerns
    
    Args:
        ingredient_name: Name of ingredient to look up
        current_user: Authenticated user
    
    Returns:
        IngredientDetail with complete information
    """
    try:
        logger.info(f"Looking up ingredient '{ingredient_name}' for user {current_user.id}")
        
        # TODO: Get user's skin concerns for personalized analysis
        ingredient_detail = analyze_ingredient_safety(ingredient_name)
        
        return ingredient_detail
        
    except Exception as e:
        logger.error(f"Error looking up ingredient: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to look up ingredient"
        )


@router.post(
    "/analyze/custom",
    response_model=ProductAnalysis,
    summary="Analyze custom ingredient list",
    description="Analyze a manually entered list of ingredients"
)
async def analyze_custom_product(
    product_name: str = Query(..., description="Product name"),
    ingredients: List[str] = Query(..., description="List of ingredient names"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ProductAnalysis:
    """
    Analyze a custom ingredient list.
    
    Useful when:
    - Product not in database
    - No barcode available
    - Testing DIY formulations
    
    Args:
        product_name: Name of the product
        ingredients: List of ingredient names
        current_user: Authenticated user
        db: Database session
    
    Returns:
        ProductAnalysis with complete breakdown
    """
    try:
        logger.info(f"Analyzing custom product '{product_name}' with {len(ingredients)} ingredients")
        
        # Analyze each ingredient
        analyzed_ingredients = [
            analyze_ingredient_safety(ing) for ing in ingredients
        ]
        
        # Calculate safety score
        safety_score = calculate_safety_score(analyzed_ingredients)
        
        # Determine hazard level
        if safety_score >= 80:
            hazard_level = "low"
        elif safety_score >= 60:
            hazard_level = "moderate"
        else:
            hazard_level = "high"
        
        # Identify flagged ingredients
        flagged = [
            ing.inci_name for ing in analyzed_ingredients
            if ing.safety_rating >= 4 or ing.is_allergen or ing.is_irritant
        ]
        
        # Generate personalized warnings
        # TODO: Query user's skin concerns from database
        personalized_warnings = []
        for ing in analyzed_ingredients:
            if ing.warnings:
                personalized_warnings.extend(ing.warnings)
        
        return ProductAnalysis(
            product_name=product_name,
            overall_safety_score=round(safety_score, 1),
            hazard_level=hazard_level,
            ingredients=analyzed_ingredients,
            total_ingredients=len(analyzed_ingredients),
            flagged_ingredients=flagged,
            personalized_warnings=list(set(personalized_warnings)),  # Remove duplicates
            is_compatible=len(flagged) == 0
        )
        
    except Exception as e:
        logger.error(f"Error analyzing custom product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze product"
        )


@router.get(
    "/search",
    summary="Search for products",
    description="Search product database by name or brand"
)
async def search_products(
    query: str = Query(..., min_length=2, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Search for products in the ingredient database.
    
    Args:
        query: Search term (product name or brand)
        category: Optional category filter
        limit: Maximum number of results
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Dictionary with search results
    """
    try:
        logger.info(f"Searching products: '{query}' (category: {category})")
        
        # TODO: Implement actual database search
        # Mock results for now
        mock_results = [
            {
                "product_id": "PROD001",
                "name": "CeraVe Hydrating Cleanser",
                "brand": "CeraVe",
                "category": "Cleanser",
                "safety_score": 85.5,
                "barcode": "3606000437128"
            },
            {
                "product_id": "PROD002",
                "name": "The Ordinary Niacinamide 10% + Zinc 1%",
                "brand": "The Ordinary",
                "category": "Serum",
                "safety_score": 92.0,
                "barcode": "769915190427"
            }
        ]
        
        return {
            "query": query,
            "total_results": len(mock_results),
            "results": mock_results[:limit]
        }
        
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search products"
        )