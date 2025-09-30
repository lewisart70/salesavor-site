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
    return {"message": "Grocery Savings App API"}

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
    """Generate recipes based on available sale ingredients"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        
        # Initialize LLM chat
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="LLM API key not configured")
        
        chat = LlmChat(
            api_key=api_key,
            session_id=f"recipe-gen-{uuid.uuid4()}",
            system_message="You are a professional chef and nutritionist helping families save money on groceries by creating delicious meals using sale ingredients. Generate detailed recipes with precise measurements and clear instructions."
        ).with_model("openai", "gpt-5")
        
        # Extract data from request
        sale_items = request.get('sale_items', [])
        dietary_preferences = request.get('dietary_preferences', [])
        servings = request.get('servings', 4)
        
        # Build ingredient list for prompt
        ingredients_text = "\n".join([f"- {item['name']} (${item['sale_price']:.2f}, was ${item['original_price']:.2f})" for item in sale_items])
        
        dietary_text = f"Dietary preferences: {', '.join(dietary_preferences)}" if dietary_preferences else "No dietary restrictions"
        
        prompt = f"""Create 3 diverse, family-friendly recipes using primarily these sale ingredients:

{ingredients_text}

{dietary_text}
Servings: {servings}

For each recipe, provide:
1. Recipe name
2. Brief description (1 sentence)
3. Detailed ingredient list with quantities
4. Step-by-step cooking instructions
5. Prep time and cook time in minutes
6. Any dietary tags (vegetarian, gluten-free, etc.)
7. Estimated total cost

Format your response as a JSON array with this structure:
[
  {{
    "name": "Recipe Name",
    "description": "Brief description",
    "ingredients": [
      {{"name": "ingredient name", "quantity": "amount", "unit": "measurement", "estimated_price": 0.00}}
    ],
    "instructions": ["Step 1", "Step 2", "Step 3"],
    "prep_time": 15,
    "cook_time": 30,
    "servings": {servings},
    "dietary_tags": ["tag1", "tag2"],
    "estimated_cost": 0.00
  }}
]

Ensure recipes are practical, economical, and use the sale ingredients effectively."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        # Parse JSON response
        import json
        try:
            recipes_data = json.loads(response)
            recipes = []
            
            for recipe_data in recipes_data:
                recipe = Recipe(
                    name=recipe_data['name'],
                    description=recipe_data['description'],
                    ingredients=recipe_data['ingredients'],
                    instructions=recipe_data['instructions'],
                    prep_time=recipe_data['prep_time'],
                    cook_time=recipe_data['cook_time'],
                    servings=recipe_data.get('servings', servings),
                    dietary_tags=recipe_data.get('dietary_tags', []),
                    estimated_cost=recipe_data.get('estimated_cost', 0.0)
                )
                recipes.append(recipe)
            
            return recipes
            
        except json.JSONDecodeError:
            # Fallback: create a simple recipe if JSON parsing fails
            return [
                Recipe(
                    name="Budget-Friendly Stir Fry",
                    description="A quick and economical meal using sale ingredients",
                    ingredients=[
                        {"name": "Ground Beef", "quantity": "1", "unit": "lb", "estimated_price": 4.99},
                        {"name": "Bell Peppers", "quantity": "2", "unit": "each", "estimated_price": 3.98},
                        {"name": "Onions", "quantity": "1", "unit": "medium", "estimated_price": 1.00}
                    ],
                    instructions=[
                        "Heat oil in a large pan over medium-high heat",
                        "Brown the ground beef, breaking it up as it cooks",
                        "Add sliced peppers and onions, cook until tender",
                        "Season with salt, pepper, and your favorite spices",
                        "Serve hot with rice or pasta"
                    ],
                    prep_time=10,
                    cook_time=15,
                    servings=servings,
                    dietary_tags=[],
                    estimated_cost=9.97
                )
            ]
            
    except Exception as e:
        logging.error(f"Error generating recipes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating recipes: {str(e)}")

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
