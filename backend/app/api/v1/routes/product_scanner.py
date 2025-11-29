"""Product Scanner API Routes

This module provides API endpoints for scanning skincare products
and receiving personalized recommendations based on skin type.

Features:
- Barcode scanning with Open Beauty Facts integration
- Ingredient analysis for skin compatibility
- Personalized product reviews based on user's skin type
- Skin concern-based ingredient warnings

Author: AI Engineering Team
Version: 1.0.0
Date: November 29, 2025
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import logging

from app.services.open_beauty_facts import OpenBeautyFactsAPI, Product

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])

# Initialize the Open Beauty Facts API client
api = OpenBeautyFactsAPI()


class IngredientAnalysis(BaseModel):
    """Model for ingredient analysis results"""
    beneficial_ingredients: List[str] = []
    ingredients_to_avoid: List[str] = []
    neutral_ingredients: List[str] = []
    compatibility_score: float = 0.0
    recommendation: str = ""
    warnings: List[str] = []


class ProductScanResponse(BaseModel):
    """Response model for product scan"""
    product: Optional[Product] = None
    analysis: Optional[IngredientAnalysis] = None
    found: bool = False
    message: str = ""


class IngredientsRequest(BaseModel):
    """Request model for ingredient analysis"""
    ingredients: List[str]
    skin_type: str
    skin_concerns: List[str] = []


def calculate_compatibility_score(
    beneficial: List[str],
    harmful: List[str],
    total_ingredients: int
) -> float:
    """Calculate compatibility score based on ingredients"""
    if total_ingredients == 0:
        return 50.0
    
    beneficial_score = len(beneficial) * 10
    harmful_penalty = len(harmful) * 15
    
    score = 70 + beneficial_score - harmful_penalty
    return max(0, min(100, score))


def generate_recommendation(score: float, skin_type: str) -> str:
    """Generate recommendation based on score"""
    if score >= 80:
        return f"Excellent choice for {skin_type} skin! This product contains ingredients well-suited for your skin type."
    elif score >= 60:
        return f"Good option for {skin_type} skin. Some ingredients may be beneficial."
    elif score >= 40:
        return f"Use with caution for {skin_type} skin. Monitor for any reactions."
    else:
        return f"Not recommended for {skin_type} skin. Contains ingredients that may cause issues."


def analyze_ingredients_for_skin_type(
    ingredients: List[str],
    skin_type: str,
    skin_concerns: List[str] = []
) -> IngredientAnalysis:
    """Analyze product ingredients based on skin type and concerns"""
    
    # Get recommendations from Open Beauty Facts API
    concerns = skin_concerns.copy()
    if skin_type:
        concerns.append(f"{skin_type}_skin")
    
    ingredient_recs = api.get_recommended_ingredients(concerns)
    
    beneficial_found = []
    harmful_found = []
    neutral = []
    warnings = []
    
    for ing in ingredients:
        ing_lower = ing.lower().replace(" ", "-").replace("_", "-")
        
        if any(b in ing_lower for b in ingredient_recs.get("beneficial", [])):
            beneficial_found.append(ing)
        elif any(a in ing_lower for a in ingredient_recs.get("avoid", [])):
            harmful_found.append(ing)
            warnings.append(f"'{ing}' may not be suitable for {skin_type} skin")
        else:
            neutral.append(ing)
    
    score = calculate_compatibility_score(
        beneficial_found,
        harmful_found,
        len(ingredients)
    )
    
    recommendation = generate_recommendation(score, skin_type)
    
    return IngredientAnalysis(
        beneficial_ingredients=beneficial_found,
        ingredients_to_avoid=harmful_found,
        neutral_ingredients=neutral,
        compatibility_score=score,
        recommendation=recommendation,
        warnings=warnings
    )


@router.get("/scan/{barcode}", response_model=ProductScanResponse)
async def scan_product(
    barcode: str,
    skin_type: str = Query(default="normal", description="User's skin type"),
    skin_concerns: str = Query(default="", description="Comma-separated skin concerns")
):
    """
    Scan a product by barcode and get personalized analysis.
    
    Args:
        barcode: Product barcode (EAN/UPC)
        skin_type: User's skin type (oily, dry, combination, sensitive, normal)
        skin_concerns: Comma-separated list of concerns (acne, aging, etc.)
    
    Returns:
        ProductScanResponse with product info and personalized analysis
    """
    try:
        # Fetch product from Open Beauty Facts
        product = await api.get_product_by_barcode(barcode)
        
        if not product:
            return ProductScanResponse(
                found=False,
                message=f"Product with barcode {barcode} not found in database"
            )
        
        # Parse skin concerns
        concerns = [c.strip() for c in skin_concerns.split(",") if c.strip()]
        
        # Analyze ingredients
        analysis = analyze_ingredients_for_skin_type(
            ingredients=product.ingredients or [],
            skin_type=skin_type,
            skin_concerns=concerns
        )
        
        return ProductScanResponse(
            product=product,
            analysis=analysis,
            found=True,
            message="Product analyzed successfully"
        )
        
    except Exception as e:
        logger.error(f"Error scanning product {barcode}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing product: {str(e)}"
        )


@router.post("/analyze-ingredients", response_model=IngredientAnalysis)
async def analyze_ingredients(request: IngredientsRequest):
    """
    Analyze a list of ingredients for skin compatibility.
    
    Args:
        request: IngredientsRequest with ingredients list and skin info
    
    Returns:
        IngredientAnalysis with compatibility score and recommendations
    """
    try:
        analysis = analyze_ingredients_for_skin_type(
            ingredients=request.ingredients,
            skin_type=request.skin_type,
            skin_concerns=request.skin_concerns
        )
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing ingredients: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing ingredients: {str(e)}"
        )


@router.get("/search")
async def search_products(
    query: str = Query(..., description="Search term"),
    skin_type: str = Query(default="normal", description="User's skin type"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50)
):
    """
    Search for products and get personalized recommendations.
    
    Args:
        query: Search term
        skin_type: User's skin type
        page: Page number
        page_size: Results per page
    
    Returns:
        List of products with compatibility analysis
    """
    try:
        products = await api.search_products(
            query=query,
            page=page,
            page_size=page_size
        )
        
        results = []
        for product in products:
            analysis = analyze_ingredients_for_skin_type(
                ingredients=product.ingredients or [],
                skin_type=skin_type
            )
            results.append({
                "product": product,
                "analysis": analysis
            })
        
        return {
            "results": results,
            "page": page,
            "page_size": page_size,
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching products: {str(e)}"
        )


@router.get("/recommendations/{skin_type}")
async def get_product_recommendations(
    skin_type: str,
    skin_concerns: str = Query(default="", description="Comma-separated skin concerns"),
    limit: int = Query(default=10, ge=1, le=50)
):
    """
    Get product recommendations based on skin type and concerns.
    
    Args:
        skin_type: User's skin type
        skin_concerns: Comma-separated list of concerns
        limit: Maximum number of recommendations
    
    Returns:
        List of recommended products
    """
    try:
        concerns = [c.strip() for c in skin_concerns.split(",") if c.strip()]
        
        products = await api.get_products_for_skin_type(
            skin_type=skin_type,
            skin_concerns=concerns,
            limit=limit
        )
        
        results = []
        for product in products:
            analysis = analyze_ingredients_for_skin_type(
                ingredients=product.ingredients or [],
                skin_type=skin_type,
                skin_concerns=concerns
            )
            results.append({
                "product": product,
                "analysis": analysis
            })
        
        # Sort by compatibility score
        results.sort(
            key=lambda x: x["analysis"].compatibility_score,
            reverse=True
        )
        
        return {
            "skin_type": skin_type,
            "skin_concerns": concerns,
            "recommendations": results
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting recommendations: {str(e)}"
        )
