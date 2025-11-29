import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

/// Local database service for skincare data
/// Loads bundled JSON data - no server or database costs!
class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();
  factory DatabaseService() => _instance;
  DatabaseService._internal();

  Map<String, dynamic>? _products;
  Map<String, dynamic>? _ingredients;
  Map<String, dynamic>? _skinConditions;
  bool _isInitialized = false;

  /// Initialize and load all JSON data
  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      // Load JSON files from assets
      _products = await _loadJson('assets/data/products.json');
      _ingredients = await _loadJson('assets/data/ingredients.json');
      _skinConditions = await _loadJson('assets/data/skin_conditions.json');
      
      _isInitialized = true;
      debugPrint('DatabaseService: Loaded local JSON databases');
    } catch (e) {
      debugPrint('DatabaseService: Error loading data - $e');
      // Use fallback empty data
      _products = {'products': [], 'categories': [], 'skin_types': [], 'concerns': []};
      _ingredients = {'ingredients': [], 'ingredient_conflicts': []};
      _skinConditions = {'skin_conditions': [], 'analysis_zones': []};
      _isInitialized = true;
    }
  }

  /// Load a JSON file from assets
  Future<Map<String, dynamic>> _loadJson(String path) async {
    try {
      final String response = await rootBundle.loadString(path);
      return json.decode(response) as Map<String, dynamic>;
    } catch (e) {
      debugPrint('Failed to load $path: $e');
      return {};
    }
  }

  /// Get all products
  List<Product> getProducts() {
    if (_products == null) return [];
    final productList = _products!['products'] as List<dynamic>? ?? [];
    return productList.map((p) => Product.fromJson(p)).toList();
  }

  /// Get products by category
  List<Product> getProductsByCategory(String category) {
    return getProducts().where((p) => p.category == category).toList();
  }

  /// Get products for skin type
  List<Product> getProductsForSkinType(String skinType) {
    return getProducts().where((p) => p.skinTypes.contains(skinType)).toList();
  }

  /// Get products for a skin concern
  List<Product> getProductsForConcern(String concern) {
    return getProducts().where((p) => p.concerns.contains(concern)).toList();
  }

  /// Get all ingredients
  List<Ingredient> getIngredients() {
    if (_ingredients == null) return [];
    final ingredientList = _ingredients!['ingredients'] as List<dynamic>? ?? [];
    return ingredientList.map((i) => Ingredient.fromJson(i)).toList();
  }

  /// Get ingredient by name
  Ingredient? getIngredientByName(String name) {
    try {
      return getIngredients().firstWhere(
        (i) => i.name.toLowerCase() == name.toLowerCase() ||
               i.aliases.any((a) => a.toLowerCase() == name.toLowerCase()),
      );
    } catch (_) {
      return null;
    }
  }

  /// Get ingredient conflicts
  List<IngredientConflict> getIngredientConflicts() {
    if (_ingredients == null) return [];
    final conflicts = _ingredients!['ingredient_conflicts'] as List<dynamic>? ?? [];
    return conflicts.map((c) => IngredientConflict.fromJson(c)).toList();
  }

  /// Get all skin conditions
  List<SkinCondition> getSkinConditions() {
    if (_skinConditions == null) return [];
    final conditionList = _skinConditions!['skin_conditions'] as List<dynamic>? ?? [];
    return conditionList.map((c) => SkinCondition.fromJson(c)).toList();
  }

  /// Get recommended products for a skin condition
  List<Product> getRecommendedProducts(String conditionName) {
    final condition = getSkinConditions().firstWhere(
      (c) => c.name.toLowerCase() == conditionName.toLowerCase(),
      orElse: () => SkinCondition.empty(),
    );

    if (condition.isEmpty) return [];

    return getProducts().where((product) {
      return product.ingredients.any(
        (i) => condition.recommendedIngredients.contains(i),
      );
    }).toList();
  }

  /// Get available skin types
  List<String> getSkinTypes() {
    if (_products == null) return [];
    return List<String>.from(_products!['skin_types'] ?? []);
  }

  /// Get available concerns
  List<String> getConcerns() {
    if (_products == null) return [];
    return List<String>.from(_products!['concerns'] ?? []);
  }

  /// Get product categories
  List<String> getCategories() {
    if (_products == null) return [];
    return List<String>.from(_products!['categories'] ?? []);
  }
}

// Data Models

class Product {
  final String id;
  final String name;
  final String brand;
  final String category;
  final List<String> skinTypes;
  final List<String> concerns;
  final List<String> ingredients;
  final double price;
  final double rating;
  final String imageUrl;

  Product({
    required this.id,
    required this.name,
    required this.brand,
    required this.category,
    required this.skinTypes,
    required this.concerns,
    required this.ingredients,
    required this.price,
    required this.rating,
    required this.imageUrl,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      brand: json['brand'] ?? '',
      category: json['category'] ?? '',
      skinTypes: List<String>.from(json['skin_types'] ?? []),
      concerns: List<String>.from(json['concerns'] ?? []),
      ingredients: List<String>.from(json['ingredients'] ?? []),
      price: (json['price'] ?? 0).toDouble(),
      rating: (json['rating'] ?? 0).toDouble(),
      imageUrl: json['image_url'] ?? '',
    );
  }
}

class Ingredient {
  final String id;
  final String name;
  final List<String> aliases;
  final String category;
  final List<String> benefits;
  final List<String> skinTypes;
  final int safetyRating;
  final int comedogenicRating;
  final List<String>? warnings;

  Ingredient({
    required this.id,
    required this.name,
    required this.aliases,
    required this.category,
    required this.benefits,
    required this.skinTypes,
    required this.safetyRating,
    required this.comedogenicRating,
    this.warnings,
  });

  factory Ingredient.fromJson(Map<String, dynamic> json) {
    return Ingredient(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      aliases: List<String>.from(json['aliases'] ?? []),
      category: json['category'] ?? '',
      benefits: List<String>.from(json['benefits'] ?? []),
      skinTypes: List<String>.from(json['skin_types'] ?? []),
      safetyRating: json['safety_rating'] ?? 0,
      comedogenicRating: json['comedogenic_rating'] ?? 0,
      warnings: json['warnings'] != null ? List<String>.from(json['warnings']) : null,
    );
  }
}

class IngredientConflict {
  final List<String> ingredients;
  final String reason;

  IngredientConflict({required this.ingredients, required this.reason});

  factory IngredientConflict.fromJson(Map<String, dynamic> json) {
    return IngredientConflict(
      ingredients: List<String>.from(json['ingredients'] ?? []),
      reason: json['reason'] ?? '',
    );
  }
}

class SkinCondition {
  final String id;
  final String name;
  final List<String> severityLevels;
  final List<String> symptoms;
  final List<String> recommendedIngredients;
  final List<String> avoidIngredients;
  final String treatmentDuration;

  bool get isEmpty => id.isEmpty;

  SkinCondition({
    required this.id,
    required this.name,
    required this.severityLevels,
    required this.symptoms,
    required this.recommendedIngredients,
    required this.avoidIngredients,
    required this.treatmentDuration,
  });

  factory SkinCondition.empty() {
    return SkinCondition(
      id: '',
      name: '',
      severityLevels: [],
      symptoms: [],
      recommendedIngredients: [],
      avoidIngredients: [],
      treatmentDuration: '',
    );
  }

  factory SkinCondition.fromJson(Map<String, dynamic> json) {
    return SkinCondition(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      severityLevels: List<String>.from(json['severity_levels'] ?? []),
      symptoms: List<String>.from(json['symptoms'] ?? []),
      recommendedIngredients: List<String>.from(json['recommended_ingredients'] ?? []),
      avoidIngredients: List<String>.from(json['avoid_ingredients'] ?? []),
      treatmentDuration: json['treatment_duration'] ?? '',
    );
  }
}
