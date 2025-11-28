"""Open Beauty Facts API Integration Service

This module provides integration with the Open Beauty Facts database
for accessing cosmetic product information and ingredients.

API Documentation: https://wiki.openfoodfacts.org/API/OpenBeautyFacts
"""

import httpx
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class Product(BaseModel):
    """Cosmetic product model"""
    barcode: Optional[str] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    categories: Optional[List[str]] = []
    ingredients: Optional[List[str]] = []
    ingredients_text: Optional[str] = None
    image_url: Optional[str] = None
    

class Ingredient(BaseModel):
    """Ingredient model"""
    name: str
    function: Optional[str] = None
    safety_level: Optional[str] = None  # safe, moderate, caution
    description: Optional[str] = None


class OpenBeautyFactsAPI:
    """
    Client for Open Beauty Facts API
    
    Free database with 100,000+ cosmetic products
    No API key required!
    """
    
    BASE_URL = "https://world.openbeautyfacts.org"
    API_VERSION = "v2"
    
    # Ingredient mappings for skin concerns
    SKIN_CONCERN_INGREDIENTS = {
        "acne": {
            "beneficial": ["salicylic-acid", "benzoyl-peroxide", "niacinamide", "tea-tree-oil", "zinc"],
            "avoid": ["coconut-oil", "cocoa-butter", "isopropyl-myristate"]
        },
        "dry_skin": {
            "beneficial": ["hyaluronic-acid", "glycerin", "ceramides", "squalane", "shea-butter"],
            "avoid": ["alcohol-denat", "fragrance"]
        },
        "oily_skin": {
            "beneficial": ["niacinamide", "salicylic-acid", "clay", "charcoal", "witch-hazel"],
            "avoid": ["mineral-oil", "petrolatum", "coconut-oil"]
        },
        "sensitive_skin": {
            "beneficial": ["aloe-vera", "chamomile", "centella-asiatica", "oat-extract", "allantoin"],
            "avoid": ["fragrance", "essential-oils", "alcohol-denat", "menthol"]
        },
        "anti_aging": {
            "beneficial": ["retinol", "vitamin-c", "peptides", "hyaluronic-acid", "niacinamide"],
            "avoid": []
        },
        "hyperpigmentation": {
            "beneficial": ["vitamin-c", "niacinamide", "arbutin", "kojic-acid", "azelaic-acid"],
            "avoid": []
        }
    }
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def get_product_by_barcode(self, barcode: str) -> Optional[Product]:
        """
        Get product details by barcode
        
        Args:
            barcode: Product barcode (EAN/UPC)
            
        Returns:
            Product object or None if not found
        """
        try:
            url = f"{self.BASE_URL}/api/{self.API_VERSION}/product/{barcode}.json"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == 1:
                product_data = data.get("product", {})
                return Product(
                    barcode=barcode,
                    name=product_data.get("product_name"),
                    brand=product_data.get("brands"),
                    categories=product_data.get("categories_tags", []),
                    ingredients=product_data.get("ingredients_tags", []),
                    ingredients_text=product_data.get("ingredients_text"),
                    image_url=product_data.get("image_url")
                )
            return None
        except Exception as e:
            logger.error(f"Error fetching product {barcode}: {e}")
            return None
    
    async def search_products(
        self,
        query: Optional[str] = None,
        brand: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[Product]:
        """
        Search for products
        
        Args:
            query: Search term
            brand: Filter by brand
            category: Filter by category
            page: Page number
            page_size: Results per page
            
        Returns:
            List of Product objects
        """
        try:
            params = {
                "page": page,
                "page_size": page_size,
                "json": 1
            }
            
            if query:
                params["search_terms"] = query
            if brand:
                params["brands_tags"] = brand
            if category:
                params["categories_tags"] = category
            
            url = f"{self.BASE_URL}/cgi/search.pl"
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            products = []
            for item in data.get("products", []):
                products.append(Product(
                    barcode=item.get("code"),
                    name=item.get("product_name"),
                    brand=item.get("brands"),
                    categories=item.get("categories_tags", []),
                    ingredients=item.get("ingredients_tags", []),
                    ingredients_text=item.get("ingredients_text"),
                    image_url=item.get("image_url")
                ))
            return products
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return []
    
    async def get_products_by_ingredient(self, ingredient: str) -> List[Product]:
        """
        Get products containing a specific ingredient
        
        Args:
            ingredient: Ingredient name (e.g., "hyaluronic-acid")
            
        Returns:
            List of Product objects
        """
        try:
            url = f"{self.BASE_URL}/ingredient/{ingredient}.json"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            products = []
            for item in data.get("products", []):
                products.append(Product(
                    barcode=item.get("code"),
                    name=item.get("product_name"),
                    brand=item.get("brands"),
                    ingredients=item.get("ingredients_tags", [])
                ))
            return products
        except Exception as e:
            logger.error(f"Error fetching products by ingredient {ingredient}: {e}")
            return []
    
    async def get_all_ingredients(self) -> List[str]:
        """
        Get list of all known ingredients
        
        Returns:
            List of ingredient names
        """
        try:
            url = f"{self.BASE_URL}/ingredients.json"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            return [tag.get("name") for tag in data.get("tags", [])]
        except Exception as e:
            logger.error(f"Error fetching ingredients: {e}")
            return []
    
    def get_recommended_ingredients(self, skin_concerns: List[str]) -> Dict[str, List[str]]:
        """
        Get recommended and ingredients to avoid based on skin concerns
        
        Args:
            skin_concerns: List of skin concerns (e.g., ["acne", "oily_skin"])
            
        Returns:
            Dict with 'beneficial' and 'avoid' ingredient lists
        """
        beneficial = set()
        avoid = set()
        
        for concern in skin_concerns:
            if concern in self.SKIN_CONCERN_INGREDIENTS:
                mapping = self.SKIN_CONCERN_INGREDIENTS[concern]
                beneficial.update(mapping.get("beneficial", []))
                avoid.update(mapping.get("avoid", []))
        
        return {
            "beneficial": list(beneficial),
            "avoid": list(avoid)
        }
    
    async def get_products_for_skin_type(
        self,
        skin_type: str,
        skin_concerns: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Product]:
        """
        Get product recommendations based on skin type and concerns
        
        Args:
            skin_type: oily, dry, combination, sensitive, normal
            skin_concerns: Optional list of concerns like acne, aging, etc.
            limit: Maximum number of products to return
            
        Returns:
            List of recommended Product objects
        """
        concerns = skin_concerns or []
        concerns.append(f"{skin_type}_skin")
        
        ingredient_rec = self.get_recommended_ingredients(concerns)
        beneficial = ingredient_rec["beneficial"]
        
        all_products = []
        for ingredient in beneficial[:3]:  # Search top 3 beneficial ingredients
            products = await self.get_products_by_ingredient(ingredient)
            all_products.extend(products)
        
        # Remove duplicates and limit
        seen = set()
        unique_products = []
        for p in all_products:
            if p.barcode and p.barcode not in seen:
                seen.add(p.barcode)
                unique_products.append(p)
                if len(unique_products) >= limit:
                    break
        
        return unique_products


# Singleton instance
open_beauty_facts_api = OpenBeautyFactsAPI()


# Example usage
async def main():
    api = OpenBeautyFactsAPI()
    
    # Search for products
    products = await api.search_products(query="moisturizer", page_size=5)
    print(f"Found {len(products)} products")
    
    # Get recommendations for oily skin with acne
    recommendations = await api.get_products_for_skin_type(
        skin_type="oily",
        skin_concerns=["acne"],
        limit=5
    )
    print(f"Recommendations: {len(recommendations)} products")
    
    await api.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())