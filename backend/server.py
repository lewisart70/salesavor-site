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
    age: Optional[int] = None
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
    age: Optional[int] = None
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
    age: Optional[int] = None
    household_size: Optional[int] = None
    dietary_preferences: Optional[List[str]] = None
    food_allergies: Optional[List[str]] = None
    cuisine_preferences: Optional[List[str]] = None
    budget_range: Optional[str] = None
    cooking_skill: Optional[str] = None
    preferred_meal_types: Optional[List[str]] = None

class StoreLocation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    chain: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    distance_km: Optional[float] = None

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

# Mock data for Canadian grocery stores
CANADIAN_STORES = [
    {"name": "Loblaws Superstore", "chain": "Loblaws", "address": "123 King Street, Toronto, ON", "latitude": 43.6532, "longitude": -79.3832, "phone": "(416) 555-0123"},
    {"name": "Metro Plus", "chain": "Metro", "address": "456 Queen Street, Toronto, ON", "latitude": 43.6542, "longitude": -79.3822, "phone": "(416) 555-0124"},
    {"name": "Food Basics", "chain": "Food Basics", "address": "789 Dundas Street, Toronto, ON", "latitude": 43.6552, "longitude": -79.3812, "phone": "(416) 555-0125"},
    {"name": "Walmart Supercentre", "chain": "Walmart", "address": "321 Bloor Street, Toronto, ON", "latitude": 43.6562, "longitude": -79.3802, "phone": "(416) 555-0126"},
    {"name": "Sobeys Urban Fresh", "chain": "Sobeys", "address": "654 College Street, Toronto, ON", "latitude": 43.6572, "longitude": -79.3792, "phone": "(416) 555-0127"},
    {"name": "Costco Wholesale", "chain": "Costco", "address": "987 Yonge Street, Toronto, ON", "latitude": 43.6582, "longitude": -79.3782, "phone": "(416) 555-0128"},
    {"name": "FreshMart", "chain": "FreshMart", "address": "147 Spadina Avenue, Toronto, ON", "latitude": 43.6592, "longitude": -79.3772, "phone": "(416) 555-0129"},
    {"name": "ValueMart", "chain": "ValueMart", "address": "258 Bathurst Street, Toronto, ON", "latitude": 43.6602, "longitude": -79.3762, "phone": "(416) 555-0130"},
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
    return {"message": "GoodBasket API - Your smart grocery savings companion"}

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
    """Generate optimized grocery list based on selected recipes and nearby stores"""
    user_location = UserLocation(**request['user_location'])
    selected_recipes = request['selected_recipes']
    servings_multiplier = request.get('servings_multiplier', 1.0)
    
    # Get nearby stores
    nearby_stores = []
    for store_data in CANADIAN_STORES:
        distance = calculate_distance(
            user_location.latitude, user_location.longitude,
            store_data["latitude"], store_data["longitude"]
        )
        if distance <= 25:
            store = StoreLocation(**store_data, distance_km=round(distance, 1))
            nearby_stores.append(store)
    
    # Generate grocery list items (simplified for MVP)
    items = []
    total_cost = 0.0
    total_savings = 0.0
    
    for item_data in MOCK_SALE_ITEMS[:6]:  # Limit to first 6 items for demo
        if nearby_stores:
            store = nearby_stores[0]  # Use closest store for simplicity
            item = GroceryListItem(
                ingredient=item_data['name'],
                quantity=f"{servings_multiplier:.1f} {item_data['unit']}",
                store_name=store.name,
                store_id=store.id,
                price=item_data['original_price'] * servings_multiplier,
                is_on_sale=True,
                sale_price=item_data['sale_price'] * servings_multiplier
            )
            items.append(item)
            total_cost += item.sale_price if item.sale_price else item.price
            if item.is_on_sale and item.sale_price:
                total_savings += (item.price - item.sale_price)
    
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
