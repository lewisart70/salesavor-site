from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import math

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class UserLocation(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None

class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    email: Optional[str] = None
    household_size: int = 4
    dietary_preferences: List[str] = []  # e.g., ["vegetarian", "gluten-free", "dairy-free"]
    food_allergies: List[str] = []  # e.g., ["nuts", "shellfish"]
    cuisine_preferences: List[str] = []  # e.g., ["italian", "asian", "mexican"]
    budget_range: str = "moderate"  # "budget", "moderate", "premium"
    cooking_skill: str = "beginner"  # "beginner", "intermediate", "advanced"
    preferred_meal_types: List[str] = ["dinner"]  # "breakfast", "lunch", "dinner", "snacks"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserProfileCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    household_size: int = 4
    dietary_preferences: List[str] = []
    food_allergies: List[str] = []
    cuisine_preferences: List[str] = []
    budget_range: str = "moderate"
    cooking_skill: str = "beginner"
    preferred_meal_types: List[str] = ["dinner"]

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    household_size: Optional[int] = None
    dietary_preferences: Optional[List[str]] = None
    food_allergies: Optional[List[str]] = None
    cuisine_preferences: Optional[List[str]] = None
    budget_range: Optional[str] = None
    cooking_skill: Optional[str] = None
    preferred_meal_types: Optional[List[str]] = None

class FoodGuideRecommendation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    country: str  # "US" or "Canada"
    food_group: str  # "Vegetables and Fruits", "Grain Products", "Milk and Alternatives", "Meat and Alternatives"
    daily_servings_adult: str  # e.g., "7-10 servings"
    serving_examples: List[str]  # e.g., ["1 medium apple", "125ml (1/2 cup) fresh, frozen or canned vegetables"]
    nutritional_benefits: List[str]
    special_notes: Optional[str] = None

class FlyerScrapingStatus(BaseModel):
    store_chain: str
    last_updated: datetime
    status: str  # "success", "failed", "pending"
    items_found: int
    error_message: Optional[str] = None

class StoreLocation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    chain: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    distance_km: Optional[float] = None
    price_match_policy: Dict[str, Any] = {}  # Price matching information
    flyer_url: Optional[str] = None  # Link to current flyer
    logo_url: Optional[str] = None  # Store logo URL
    brand_color: Optional[str] = None  # Brand primary color

class SaleItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    original_price: float
    sale_price: float
    discount_percentage: float
    store_id: str
    category: str
    unit: str = "each"
    valid_until: datetime

class WeeklyFlyer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    store_chain: str
    store_location: str
    flyer_url: Optional[str] = None
    valid_from: datetime
    valid_until: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    items: List[SaleItem] = []

class Recipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    ingredients: List[Dict[str, Any]]
    instructions: List[str]
    prep_time: int  # minutes
    cook_time: int  # minutes
    servings: int = 4
    dietary_tags: List[str] = []
    estimated_cost: float = 0.0

class GroceryListItem(BaseModel):
    ingredient: str
    quantity: str
    store_name: str
    store_id: str
    price: float
    is_on_sale: bool = False
    sale_price: Optional[float] = None

class GroceryList(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_location: UserLocation
    selected_recipes: List[str]  # recipe IDs
    items: List[GroceryListItem]
    total_cost: float
    total_savings: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Canadian and American Food Guide Data
CANADIAN_FOOD_GUIDE = [
    {
        "country": "Canada",
        "food_group": "Vegetables and Fruits",
        "daily_servings_adult": "7-10 servings",
        "serving_examples": [
            "1 medium apple, orange, or pear",
            "125ml (1/2 cup) fresh, frozen or canned vegetables",
            "250ml (1 cup) raw leafy vegetables",
            "125ml (1/2 cup) 100% fruit juice"
        ],
        "nutritional_benefits": [
            "High in vitamins A and C",
            "Good source of folate",
            "High in fiber",
            "Low in fat and calories"
        ],
        "special_notes": "Choose vegetables and fruits more often than juice"
    },
    {
        "country": "Canada", 
        "food_group": "Grain Products",
        "daily_servings_adult": "6-8 servings",
        "serving_examples": [
            "1 slice bread",
            "30g cold cereal",
            "175ml (3/4 cup) hot cereal",
            "125ml (1/2 cup) pasta or rice"
        ],
        "nutritional_benefits": [
            "Good source of B vitamins",
            "Source of fiber",
            "Provides carbohydrates for energy",
            "Iron and other minerals"
        ],
        "special_notes": "Make at least half of your grain products whole grain each day"
    },
    {
        "country": "Canada",
        "food_group": "Milk and Alternatives", 
        "daily_servings_adult": "2-3 servings",
        "serving_examples": [
            "250ml (1 cup) milk",
            "175ml (3/4 cup) yogurt",
            "50g (1.5 oz) cheese",
            "250ml (1 cup) fortified soy beverage"
        ],
        "nutritional_benefits": [
            "Excellent source of calcium",
            "Good source of protein",
            "Source of vitamin A and D",
            "Riboflavin and vitamin B12"
        ],
        "special_notes": "Choose lower fat milk products most often"
    },
    {
        "country": "Canada",
        "food_group": "Meat and Alternatives",
        "daily_servings_adult": "2-3 servings", 
        "serving_examples": [
            "75g (2.5 oz) cooked meat, poultry or fish",
            "175ml (3/4 cup) cooked beans",
            "30ml (2 tbsp) peanut butter",
            "2 eggs"
        ],
        "nutritional_benefits": [
            "Excellent source of protein",
            "Good source of iron",
            "Source of zinc and B vitamins",
            "Essential amino acids"
        ],
        "special_notes": "Choose lean meat and alternatives prepared with little or no added fat or salt"
    }
]

AMERICAN_FOOD_GUIDE = [
    {
        "country": "US",
        "food_group": "Vegetables",
        "daily_servings_adult": "2-3 cups",
        "serving_examples": [
            "1 cup raw or cooked vegetables",
            "2 cups raw leafy greens",
            "1 cup vegetable juice"
        ],
        "nutritional_benefits": [
            "Rich in vitamins A, C, and K",
            "Good source of fiber",
            "Provide folate and potassium",
            "Low in calories"
        ],
        "special_notes": "Vary your vegetables - choose from all subgroups"
    },
    {
        "country": "US",
        "food_group": "Fruits", 
        "daily_servings_adult": "1.5-2 cups",
        "serving_examples": [
            "1 cup fresh fruit",
            "1 cup 100% fruit juice", 
            "1/2 cup dried fruit"
        ],
        "nutritional_benefits": [
            "Excellent source of vitamin C",
            "Good source of fiber",
            "Provide potassium",
            "Natural antioxidants"
        ],
        "special_notes": "Choose whole fruits over juice when possible"
    },
    {
        "country": "US",
        "food_group": "Grains",
        "daily_servings_adult": "6-8 ounce equivalents",
        "serving_examples": [
            "1 slice bread",
            "1 cup ready-to-eat cereal",
            "1/2 cup cooked rice or pasta"
        ],
        "nutritional_benefits": [
            "Good source of B vitamins",
            "Provide fiber (whole grains)",
            "Source of iron",
            "Carbohydrates for energy"
        ],
        "special_notes": "Make at least half your grains whole grains"
    },
    {
        "country": "US",
        "food_group": "Protein Foods",
        "daily_servings_adult": "5-6.5 ounce equivalents",
        "serving_examples": [
            "1 oz cooked meat, poultry, or fish",
            "1 egg",
            "1 tbsp peanut butter",
            "1/4 cup cooked beans"
        ],
        "nutritional_benefits": [
            "Complete proteins",
            "Good source of iron",
            "Provide zinc and B vitamins",
            "Essential amino acids"
        ],
        "special_notes": "Choose a variety of protein foods including seafood"
    },
    {
        "country": "US",
        "food_group": "Dairy",
        "daily_servings_adult": "3 cups",
        "serving_examples": [
            "1 cup milk",
            "8 oz yogurt",
            "1.5 oz natural cheese"
        ],
        "nutritional_benefits": [
            "Excellent source of calcium",
            "Good source of protein",
            "Provides vitamin D",
            "Source of potassium"
        ],
        "special_notes": "Choose low-fat or fat-free dairy products"
    }
]

# Mock data for Canadian grocery stores
# Real Canadian grocery chain flyer URLs (updated weekly)
FLYER_URLS = {
    "Loblaws": "https://www.loblaws.ca/print-flyer",
    "Metro": "https://www.metro.ca/en/flyer",
    "Walmart": "https://www.walmart.ca/en/flyer?icid=dept_flyout_other_all_flyers_30792_LV3AV1UKYE",
    "Sobeys": "https://www.sobeys.com/flyer",
    "FreshCo": "https://www.freshco.com/flyer",
    "FoodBasics": "https://www.foodbasics.ca/flyer",
    "NoFrills": "https://www.nofrills.ca/print-flyer",
    "Independent": "https://www.yourindependentgrocer.ca/print-flyer"
}

# Enhanced store data with flyer URLs
CANADIAN_STORES = [
    {
        "name": "Loblaws Superstore", 
        "chain": "Loblaws", 
        "address": "123 King Street, Toronto, ON", 
        "latitude": 43.6532, 
        "longitude": -79.3832, 
        "phone": "(416) 555-0123",
        "price_match_policy": {
            "has_price_match": True,
            "policy_name": "We'll Match It!",
            "description": "We'll match any local competitor's advertised price",
            "conditions": ["Valid local competitor flyer required", "Same product brand and size", "Within 25km radius"],
            "excluded_stores": ["Costco", "Wholesale clubs"],
            "match_percentage": 100,
            "additional_discount": 0
        },
        "flyer_url": "https://www.loblaws.ca/print-flyer",
        "logo_url": "https://via.placeholder.com/48x48/FF6600/FFFFFF?text=L",
        "brand_color": "#FF6600"
    },
    {
        "name": "Metro Plus", 
        "chain": "Metro", 
        "address": "456 Queen Street, Toronto, ON", 
        "latitude": 43.6542, 
        "longitude": -79.3822, 
        "phone": "(416) 555-0124",
        "price_match_policy": {
            "has_price_match": True,
            "policy_name": "Metro Price Match",
            "description": "We match competitor prices on identical items",
            "conditions": ["Valid competitor flyer", "Same brand and size", "Local competitors only"],
            "excluded_stores": ["Warehouse stores", "Online retailers"],
            "match_percentage": 100,
            "additional_discount": 0
        },
        "flyer_url": "https://www.metro.ca/en/flyer",
        "logo_url": "https://via.placeholder.com/48x48/0066CC/FFFFFF?text=M",
        "brand_color": "#0066CC"
    },
    {
        "name": "Food Basics", 
        "chain": "Food Basics", 
        "address": "789 Dundas Street, Toronto, ON", 
        "latitude": 43.6552, 
        "longitude": -79.3812, 
        "phone": "(416) 555-0125",
        "price_match_policy": {
            "has_price_match": False,
            "policy_name": "No Price Match",
            "description": "Everyday low prices - no price matching needed",
            "conditions": [],
            "excluded_stores": [],
            "match_percentage": 0,
            "additional_discount": 0
        },
        "flyer_url": "https://www.foodbasics.ca/flyer",
        "logo_url": "https://via.placeholder.com/48x48/FF9900/FFFFFF?text=FB",
        "brand_color": "#FF9900"
    },
    {
        "name": "Walmart Supercentre", 
        "chain": "Walmart", 
        "address": "321 Bloor Street, Toronto, ON", 
        "latitude": 43.6562, 
        "longitude": -79.3802, 
        "phone": "(416) 555-0126",
        "price_match_policy": {
            "has_price_match": True,
            "policy_name": "Ad Match Guarantee",
            "description": "We'll match any local competitor's advertised price",
            "conditions": ["Valid local competitor ad", "Identical product", "Local store within 25km"],
            "excluded_stores": ["Membership clubs", "Online-only retailers"],
            "match_percentage": 100,
            "additional_discount": 0
        },
        "flyer_url": "https://www.walmart.ca/en/flyer?icid=dept_flyout_other_all_flyers_30792_LV3AV1UKYE"
    },
    {
        "name": "Sobeys Urban Fresh", 
        "chain": "Sobeys", 
        "address": "654 College Street, Toronto, ON", 
        "latitude": 43.6572, 
        "longitude": -79.3792, 
        "phone": "(416) 555-0127",
        "price_match_policy": {
            "has_price_match": True,
            "policy_name": "Price Match Promise",
            "description": "We'll beat any competitor's price by 10%",
            "conditions": ["Valid competitor flyer", "Same product", "Local competitors"],
            "excluded_stores": ["Wholesale clubs", "Independent stores"],
            "match_percentage": 100,
            "additional_discount": 10
        },
        "flyer_url": "https://www.sobeys.com/flyer"
    },
    {
        "name": "Costco Wholesale", 
        "chain": "Costco", 
        "address": "987 Yonge Street, Toronto, ON", 
        "latitude": 43.6582, 
        "longitude": -79.3782, 
        "phone": "(416) 555-0128",
        "price_match_policy": {
            "has_price_match": False,
            "policy_name": "No Price Match",
            "description": "Membership warehouse pricing - no price matching",
            "conditions": [],
            "excluded_stores": [],
            "match_percentage": 0,
            "additional_discount": 0
        },
        "flyer_url": "https://www.costco.ca/warehouse-locations"
    },
    {
        "name": "FreshMart", 
        "chain": "FreshMart", 
        "address": "147 Spadina Avenue, Toronto, ON", 
        "latitude": 43.6592, 
        "longitude": -79.3772, 
        "phone": "(416) 555-0129",
        "price_match_policy": {
            "has_price_match": True,
            "policy_name": "Best Price Guarantee",
            "description": "We'll match and beat competitor prices by 5%",
            "conditions": ["Valid competitor ad", "Same item", "Within city limits"],
            "excluded_stores": ["Warehouse stores"],
            "match_percentage": 100,
            "additional_discount": 5
        },
        "flyer_url": "https://www.foodbasics.ca/flyer"
    },
    {
        "name": "ValueMart", 
        "chain": "ValueMart", 
        "address": "258 Bathurst Street, Toronto, ON", 
        "latitude": 43.6602, 
        "longitude": -79.3762, 
        "phone": "(416) 555-0130",
        "price_match_policy": {
            "has_price_match": True,
            "policy_name": "Price Match Plus",
            "description": "We'll match competitor prices and add extra savings",
            "conditions": ["Valid local competitor flyer", "Identical product", "Local stores only"],
            "excluded_stores": ["Online retailers", "Membership stores"],
            "match_percentage": 100,
            "additional_discount": 3
        },
        "flyer_url": "https://www.nofrills.ca/print-flyer"
    }
]

# Mock sale items
MOCK_SALE_ITEMS = [
    {"name": "Ground Beef (1 lb)", "original_price": 6.99, "sale_price": 4.99, "discount_percentage": 29, "category": "Meat", "unit": "lb"},
    {"name": "Chicken Breast (1 lb)", "original_price": 8.99, "sale_price": 5.99, "discount_percentage": 33, "category": "Meat", "unit": "lb"},
    {"name": "Pasta (500g)", "original_price": 2.49, "sale_price": 1.49, "discount_percentage": 40, "category": "Pantry", "unit": "package"},
    {"name": "Tomatoes (1 lb)", "original_price": 3.99, "sale_price": 2.49, "discount_percentage": 38, "category": "Produce", "unit": "lb"},
    {"name": "Onions (3 lb bag)", "original_price": 4.49, "sale_price": 2.99, "discount_percentage": 33, "category": "Produce", "unit": "bag"},
    {"name": "Rice (2 kg)", "original_price": 5.99, "sale_price": 3.99, "discount_percentage": 33, "category": "Pantry", "unit": "bag"},
    {"name": "Canned Tomatoes (796ml)", "original_price": 1.99, "sale_price": 1.29, "discount_percentage": 35, "category": "Pantry", "unit": "can"},
    {"name": "Bell Peppers (each)", "original_price": 2.99, "sale_price": 1.99, "discount_percentage": 33, "category": "Produce", "unit": "each"},
    {"name": "Carrots (2 lb bag)", "original_price": 2.99, "sale_price": 1.99, "discount_percentage": 33, "category": "Produce", "unit": "bag"},
    {"name": "Potatoes (5 lb bag)", "original_price": 4.99, "sale_price": 2.99, "discount_percentage": 40, "category": "Produce", "unit": "bag"},
]

# Utility functions
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) * math.sin(delta_lon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def prepare_for_mongo(data):
    """Convert Python objects to MongoDB-compatible format"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, dict):
                data[key] = prepare_for_mongo(value)
            elif isinstance(value, list):
                data[key] = [prepare_for_mongo(item) if isinstance(item, dict) else item for item in value]
    return data

# API Routes
@api_router.get("/")
async def root():
    return {"message": "SaleSavor API - Your smart grocery savings companion"}

@api_router.post("/stores/nearby", response_model=List[StoreLocation])
async def get_nearby_stores(location: UserLocation, radius_km: int = 25):
    """Get grocery stores within specified radius"""
    nearby_stores = []
    
    for store_data in CANADIAN_STORES:
        distance = calculate_distance(
            location.latitude, location.longitude,
            store_data["latitude"], store_data["longitude"]
        )
        
        if distance <= radius_km:
            store = StoreLocation(
                **store_data,
                distance_km=round(distance, 1)
            )
            nearby_stores.append(store)
    
    # Sort by distance
    nearby_stores.sort(key=lambda x: x.distance_km)
    return nearby_stores

@api_router.get("/stores/{store_id}/sales", response_model=List[SaleItem])
async def get_store_sales(store_id: str):
    """Get current sale items for a specific store"""
    sale_items = []
    
    for item_data in MOCK_SALE_ITEMS:
        item = SaleItem(
            **item_data,
            store_id=store_id,
            valid_until=datetime.now(timezone.utc) + timedelta(days=7)  # Valid for a week
        )
        sale_items.append(item)
    
    return sale_items

@api_router.post("/recipes/generate", response_model=List[Recipe])
async def generate_recipes(request: Dict[str, Any]):
    """Generate recipes based on available sale ingredients and user profile"""
    try:
        # Extract data from request
        sale_items = request.get('sale_items', [])
        dietary_preferences = request.get('dietary_preferences', [])
        servings = request.get('servings', 4)
        profile_id = request.get('profile_id')  # Optional profile ID
        
        # Get user profile if provided
        user_profile = None
        if profile_id:
            try:
                profile_data = await db.user_profiles.find_one({"id": profile_id})
                if profile_data:
                    user_profile = UserProfile(**profile_data)
                    # Use profile preferences if no dietary preferences provided
                    if not dietary_preferences:
                        dietary_preferences = user_profile.dietary_preferences
                    servings = user_profile.household_size if servings == 4 else servings
            except Exception as e:
                logging.warning(f"Could not fetch user profile {profile_id}: {str(e)}")
        
        # Filter recipes based on dietary preferences
        def filter_recipes_by_diet(recipes: List[Recipe], dietary_prefs: List[str]) -> List[Recipe]:
            if not dietary_prefs:
                return recipes
            
            filtered_recipes = []
            for recipe in recipes:
                recipe_tags = [tag.lower() for tag in recipe.dietary_tags]
                # Check if recipe matches any dietary preference
                if any(pref.lower() in recipe_tags for pref in dietary_prefs):
                    filtered_recipes.append(recipe)
                # If no dietary tags but user prefers vegetarian/vegan, skip meat recipes
                elif "vegetarian" in [p.lower() for p in dietary_prefs] and "meat" in recipe.name.lower():
                    continue
                elif "vegan" in [p.lower() for p in dietary_prefs] and any(word in recipe.name.lower() for word in ["chicken", "beef", "meat", "cheese"]):
                    continue
                else:
                    filtered_recipes.append(recipe)
            
            return filtered_recipes if filtered_recipes else recipes  # Return all if none match
        
        # For demo purposes, return mock recipes with profile-based filtering
        mock_recipes = [
            Recipe(
                name="Budget-Friendly Beef Stir Fry",
                description="A quick and economical meal using ground beef and fresh vegetables",
                ingredients=[
                    {"name": "Ground Beef", "quantity": "1", "unit": "lb", "estimated_price": 4.99},
                    {"name": "Bell Peppers", "quantity": "2", "unit": "each", "estimated_price": 3.98},
                    {"name": "Onions", "quantity": "1", "unit": "medium", "estimated_price": 1.00},
                    {"name": "Rice", "quantity": "1", "unit": "cup", "estimated_price": 1.00}
                ],
                instructions=[
                    "Heat oil in a large pan over medium-high heat",
                    "Brown the ground beef, breaking it up as it cooks (5-7 minutes)",
                    "Add diced onions and cook until translucent (3 minutes)",
                    "Add sliced bell peppers and cook until tender (4 minutes)",
                    "Season with salt, pepper, and garlic powder",
                    "Serve hot over cooked rice"
                ],
                prep_time=10,
                cook_time=15,
                servings=servings,
                dietary_tags=[],
                estimated_cost=10.97
            ),
            Recipe(
                name="Chicken Breast Pasta Bake",
                description="Delicious baked pasta with tender chicken and tomatoes",
                ingredients=[
                    {"name": "Chicken Breast", "quantity": "1", "unit": "lb", "estimated_price": 5.99},
                    {"name": "Pasta", "quantity": "1", "unit": "package", "estimated_price": 1.49},
                    {"name": "Canned Tomatoes", "quantity": "2", "unit": "cans", "estimated_price": 2.58},
                    {"name": "Carrots", "quantity": "2", "unit": "large", "estimated_price": 1.00}
                ],
                instructions=[
                    "Preheat oven to 375°F (190°C)",
                    "Cook pasta according to package directions, drain",
                    "Cut chicken into bite-sized pieces and season",
                    "Cook chicken in a large skillet until golden (8 minutes)",
                    "Add diced carrots and canned tomatoes",
                    "Combine with pasta in a baking dish",
                    "Bake for 25 minutes until bubbly and golden"
                ],
                prep_time=20,
                cook_time=35,
                servings=servings,
                dietary_tags=[],
                estimated_cost=11.06
            ),
            Recipe(
                name="Hearty Vegetable Rice Bowl",
                description="Nutritious and filling vegetarian bowl with seasonal vegetables",
                ingredients=[
                    {"name": "Rice", "quantity": "2", "unit": "cups", "estimated_price": 2.00},
                    {"name": "Bell Peppers", "quantity": "3", "unit": "each", "estimated_price": 5.97},
                    {"name": "Carrots", "quantity": "3", "unit": "large", "estimated_price": 1.50},
                    {"name": "Onions", "quantity": "2", "unit": "medium", "estimated_price": 2.00}
                ],
                instructions=[
                    "Cook rice according to package directions",
                    "Heat oil in a large wok or skillet",
                    "Add sliced onions and cook until fragrant (3 minutes)",
                    "Add julienned carrots and cook for 5 minutes",
                    "Add bell pepper strips and stir-fry for 4 minutes",
                    "Season with soy sauce, garlic, and ginger",
                    "Serve vegetables over rice with fresh herbs"
                ],
                prep_time=15,
                cook_time=20,
                servings=servings,
                dietary_tags=["Vegetarian", "Vegan", "Gluten-Free"],
                estimated_cost=11.47
            ),
            Recipe(
                name="Mediterranean Quinoa Salad",
                description="Fresh and healthy gluten-free salad with Mediterranean flavors",
                ingredients=[
                    {"name": "Quinoa", "quantity": "2", "unit": "cups", "estimated_price": 3.50},
                    {"name": "Bell Peppers", "quantity": "2", "unit": "each", "estimated_price": 3.98},
                    {"name": "Tomatoes", "quantity": "3", "unit": "medium", "estimated_price": 2.49},
                    {"name": "Onions", "quantity": "1", "unit": "small", "estimated_price": 0.75}
                ],
                instructions=[
                    "Cook quinoa according to package directions and let cool",
                    "Dice bell peppers, tomatoes, and onions",
                    "Mix vegetables with cooked quinoa",
                    "Drizzle with olive oil and lemon juice",
                    "Season with salt, pepper, and dried herbs",
                    "Chill for 30 minutes before serving"
                ],
                prep_time=25,
                cook_time=15,
                servings=servings,
                dietary_tags=["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"],
                estimated_cost=10.72
            )
        ]
        
        # Filter recipes based on dietary preferences
        filtered_recipes = filter_recipes_by_diet(mock_recipes, dietary_preferences)
        
        # Return top 3 recipes
        return filtered_recipes[:3]
        
        # TODO: Uncomment below for LLM integration when API is stable
        # from emergentintegrations.llm.chat import LlmChat, UserMessage
        # 
        # api_key = os.environ.get('EMERGENT_LLM_KEY')
        # if not api_key:
        #     raise HTTPException(status_code=500, detail="LLM API key not configured")
        # 
        # chat = LlmChat(
        #     api_key=api_key,
        #     session_id=f"recipe-gen-{uuid.uuid4()}",
        #     system_message="You are a professional chef helping families save money on groceries."
        # ).with_model("openai", "gpt-4o")
        # 
        # ingredients_text = "\n".join([f"- {item['name']} (${item['sale_price']:.2f})" for item in sale_items])
        # prompt = f"Create 3 recipes using these sale ingredients:\n{ingredients_text}\nReturn JSON format with recipe details."
        # 
        # user_message = UserMessage(text=prompt)
        # response = await chat.send_message(user_message)
        # # Parse and return LLM response
            
    except Exception as e:
        logging.error(f"Error generating recipes: {str(e)}")
        # Return fallback recipes even on error
        return [
            Recipe(
                name="Simple Ground Beef Skillet",
                description="Quick and budget-friendly family meal",
                ingredients=[
                    {"name": "Ground Beef", "quantity": "1", "unit": "lb", "estimated_price": 4.99}
                ],
                instructions=["Brown ground beef", "Season and serve"],
                prep_time=5,
                cook_time=10,
                servings=servings,
                dietary_tags=[],
                estimated_cost=4.99
            )
        ]

@api_router.post("/grocery-list/generate", response_model=GroceryList)
async def generate_grocery_list(request: Dict[str, Any]):
    """Generate optimized grocery list based on selected recipes and nearby stores with price matching"""
    user_location = UserLocation(**request['user_location'])
    selected_recipes = request['selected_recipes']
    servings_multiplier = request.get('servings_multiplier', 1.0)
    
    # Get nearby stores with price match info
    nearby_stores = []
    for store_data in CANADIAN_STORES:
        distance = calculate_distance(
            user_location.latitude, user_location.longitude,
            store_data["latitude"], store_data["longitude"]
        )
        if distance <= 25:
            store = StoreLocation(**store_data, distance_km=round(distance, 1))
            nearby_stores.append(store)
    
    # Sort by distance
    nearby_stores.sort(key=lambda x: x.distance_km)
    
    # Create a comprehensive price comparison across all stores
    all_store_prices = {}
    for store in nearby_stores:
        for item_data in MOCK_SALE_ITEMS:
            item_id = item_data['name']
            if item_id not in all_store_prices:
                all_store_prices[item_id] = []
            
            all_store_prices[item_id].append({
                'store': store,
                'original_price': item_data['original_price'],
                'sale_price': item_data['sale_price'],
                'item_data': item_data
            })
    
    # Generate optimized grocery list using price matching
    items = []
    total_cost = 0.0
    total_savings = 0.0
    
    for item_id, store_prices in all_store_prices.items():
        if len(items) >= 8:  # Limit for demo
            break
            
        # Find the best price across all stores
        best_price_info = min(store_prices, key=lambda x: x['sale_price'])
        best_price = best_price_info['sale_price']
        best_original_price = best_price_info['original_price']
        
        # Find the best store to shop at (considering price matching)
        recommended_store = None
        final_price = best_price
        price_match_used = False
        
        for store in nearby_stores:
            if store.price_match_policy.get('has_price_match', False):
                # This store can price match, so we can get the best price here
                additional_discount = store.price_match_policy.get('additional_discount', 0)
                if additional_discount > 0:
                    # Store beats competitor prices by additional percentage
                    potential_price = best_price * (1 - additional_discount / 100)
                    if potential_price < final_price:
                        final_price = potential_price
                        recommended_store = store
                        price_match_used = True
                        break
                else:
                    # Store matches prices exactly
                    recommended_store = store
                    price_match_used = True
                    break
        
        # If no price matching store found, use the store with the actual best price
        if not recommended_store:
            recommended_store = best_price_info['store']
        
        # Create grocery list item
        item = GroceryListItem(
            ingredient=item_id,
            quantity=f"{servings_multiplier:.1f} {best_price_info['item_data']['unit']}",
            store_name=f"{recommended_store.name}{' (Price Match)' if price_match_used else ''}",
            store_id=recommended_store.id,
            price=best_original_price * servings_multiplier,
            is_on_sale=True,
            sale_price=final_price * servings_multiplier
        )
        
        items.append(item)
        total_cost += final_price * servings_multiplier
        total_savings += (best_original_price - final_price) * servings_multiplier
    
    grocery_list = GroceryList(
        user_location=user_location,
        selected_recipes=selected_recipes,
        items=items,
        total_cost=total_cost,
        total_savings=total_savings
    )
    
    return grocery_list

# User Profile Management Endpoints
@api_router.post("/profile", response_model=UserProfile)
async def create_profile(profile_data: UserProfileCreate):
    """Create a new user profile"""
    try:
        profile = UserProfile(**profile_data.dict())
        profile_dict = prepare_for_mongo(profile.dict())
        await db.user_profiles.insert_one(profile_dict)
        return profile
    except Exception as e:
        logging.error(f"Error creating profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating profile: {str(e)}")

@api_router.get("/profile/{profile_id}", response_model=UserProfile)
async def get_profile(profile_id: str):
    """Get user profile by ID"""
    try:
        profile_data = await db.user_profiles.find_one({"id": profile_id})
        if not profile_data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return UserProfile(**profile_data)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {str(e)}")

@api_router.put("/profile/{profile_id}", response_model=UserProfile)
async def update_profile(profile_id: str, profile_update: UserProfileUpdate):
    """Update user profile"""
    try:
        existing_profile = await db.user_profiles.find_one({"id": profile_id})
        if not existing_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Update only provided fields
        update_data = {k: v for k, v in profile_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.now(timezone.utc)
        
        update_dict = prepare_for_mongo(update_data)
        await db.user_profiles.update_one({"id": profile_id}, {"$set": update_dict})
        
        # Return updated profile
        updated_profile_data = await db.user_profiles.find_one({"id": profile_id})
        return UserProfile(**updated_profile_data)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating profile: {str(e)}")

@api_router.delete("/profile/{profile_id}")
async def delete_profile(profile_id: str):
    """Delete user profile"""
    try:
        result = await db.user_profiles.delete_one({"id": profile_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {"message": "Profile deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting profile: {str(e)}")

# Food Guide Information Endpoints
@api_router.get("/food-guide/{country}", response_model=List[FoodGuideRecommendation])
async def get_food_guide(country: str):
    """Get food guide recommendations for specified country (US or Canada)"""
    try:
        country_upper = country.upper()
        if country_upper == "CANADA":
            food_guide_data = CANADIAN_FOOD_GUIDE
        elif country_upper == "US" or country_upper == "USA":
            food_guide_data = AMERICAN_FOOD_GUIDE
        else:
            raise HTTPException(status_code=400, detail="Country must be 'Canada' or 'US'")
        
        recommendations = [FoodGuideRecommendation(**item) for item in food_guide_data]
        return recommendations
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching food guide: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching food guide: {str(e)}")

@api_router.get("/food-guide", response_model=List[FoodGuideRecommendation])
async def get_all_food_guides():
    """Get food guide recommendations for both countries"""
    try:
        all_recommendations = []
        for item in CANADIAN_FOOD_GUIDE + AMERICAN_FOOD_GUIDE:
            all_recommendations.append(FoodGuideRecommendation(**item))
        return all_recommendations
    except Exception as e:
        logging.error(f"Error fetching food guides: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching food guides: {str(e)}")

# Weekly Flyer Integration Endpoints
@api_router.get("/flyers/{store_chain}")
async def get_store_flyer_url(store_chain: str):
    """Get the current flyer URL for a specific store chain"""
    try:
        # Find the store and return its flyer URL
        for store_data in CANADIAN_STORES:
            if store_data["chain"].lower() == store_chain.lower():
                return {
                    "store_chain": store_data["chain"],
                    "store_name": store_data["name"],
                    "flyer_url": store_data.get("flyer_url", ""),
                    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "note": "Flyers typically update weekly on Thursdays"
                }
        
        raise HTTPException(status_code=404, detail=f"Store chain '{store_chain}' not found")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching flyer URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching flyer URL: {str(e)}")

@api_router.get("/flyers")
async def get_all_flyer_urls():
    """Get flyer URLs for all store chains"""
    try:
        flyers = []
        for store_data in CANADIAN_STORES:
            if store_data.get("flyer_url"):
                flyers.append({
                    "store_chain": store_data["chain"],
                    "store_name": store_data["name"],
                    "flyer_url": store_data["flyer_url"],
                    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "has_price_match": store_data.get("price_match_policy", {}).get("has_price_match", False)
                })
        return flyers
    except Exception as e:
        logging.error(f"Error fetching flyer URLs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching flyer URLs: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
