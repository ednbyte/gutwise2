from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging
import ssl
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import re


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(
    mongo_url,
    tls=True,
    tlsAllowInvalidCertificates=True,
    tlsAllowInvalidHostnames=True,
    tlsInsecure=True,
    serverSelectionTimeoutMS=30000,
    connectTimeoutMS=30000,
    socketTimeoutMS=30000,
)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="GutWise Recipe API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class Recipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    image: str
    prep_time: str
    cook_time: str
    servings: int
    difficulty: str  # Easy, Medium, Hard
    dietary_tags: List[str]  # gluten-free, dairy-free, low-fodmap, vegan, paleo, keto
    ingredients: List[str]
    instructions: List[str]
    story: str  # Personal healing story
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RecipeCreate(BaseModel):
    title: str
    description: str
    image: str
    prep_time: str
    cook_time: str
    servings: int
    difficulty: str
    dietary_tags: List[str]
    ingredients: List[str]
    instructions: List[str]
    story: str

class PersonalStory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    content: List[str]  # Array of paragraphs
    image: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DietaryFilter(BaseModel):
    id: str
    label: str
    count: int

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "GutWise Recipe API - Helping heal one recipe at a time"}

# Recipe Endpoints
@api_router.get("/recipes", response_model=List[Recipe])
async def get_recipes(
    search: Optional[str] = Query(None, description="Search recipes by title, description, or ingredients"),
    dietary_tags: Optional[str] = Query(None, description="Filter by dietary tags (comma-separated)"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
):
    query = {}
    
    # Build search query
    if search:
        search_regex = re.compile(search, re.IGNORECASE)
        query["$or"] = [
            {"title": search_regex},
            {"description": search_regex},
            {"ingredients": {"$elemMatch": {"$regex": search_regex}}}
        ]
    
    # Build dietary tags filter
    if dietary_tags:
        tags_list = [tag.strip() for tag in dietary_tags.split(",")]
        query["dietary_tags"] = {"$all": tags_list}
    
    # Execute query with pagination
    cursor = db.recipes.find(query).skip(offset)
    if limit:
        cursor = cursor.limit(limit)
    
    recipes = await cursor.to_list(length=None)
    return [Recipe(**recipe) for recipe in recipes]

@api_router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: str):
    recipe = await db.recipes.find_one({"id": recipe_id})
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return Recipe(**recipe)

@api_router.post("/recipes", response_model=Recipe)
async def create_recipe(recipe_data: RecipeCreate):
    recipe = Recipe(**recipe_data.dict())
    await db.recipes.insert_one(recipe.dict())
    return recipe

# Dietary Filter Endpoints
@api_router.get("/dietary-filters", response_model=List[DietaryFilter])
async def get_dietary_filters():
    # Aggregate dietary tag counts
    pipeline = [
        {"$unwind": "$dietary_tags"},
        {"$group": {"_id": "$dietary_tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    
    result = await db.recipes.aggregate(pipeline).to_list(length=None)
    
    # Map to readable labels
    label_map = {
        "gluten-free": "Gluten-Free",
        "dairy-free": "Dairy-Free", 
        "low-fodmap": "Low-FODMAP",
        "vegan": "Vegan",
        "paleo": "Paleo",
        "keto": "Keto"
    }
    
    filters = []
    for item in result:
        tag_id = item["_id"]
        filters.append(DietaryFilter(
            id=tag_id,
            label=label_map.get(tag_id, tag_id.title()),
            count=item["count"]
        ))
    
    return filters

# Personal Story Endpoints
@api_router.get("/personal-story", response_model=PersonalStory)
async def get_personal_story():
    story = await db.personal_stories.find_one()
    if not story:
        raise HTTPException(status_code=404, detail="Personal story not found")
    return PersonalStory(**story)

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database seeding data
SEED_RECIPES = [
    {
        "id": "1",
        "title": "Gentle Chicken and Rice Bowl",
        "description": "A soothing, easy-to-digest meal that was one of my first safe foods during recovery.",
        "image": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=600&h=400&fit=crop",
        "prep_time": "15 min",
        "cook_time": "25 min",
        "servings": 4,
        "difficulty": "Easy",
        "dietary_tags": ["gluten-free", "dairy-free", "low-fodmap"],
        "ingredients": [
            "2 cups jasmine rice",
            "4 chicken thighs (boneless, skinless)",
            "3 cups low-sodium chicken broth",
            "2 tbsp olive oil",
            "1 tsp salt",
            "1/2 tsp turmeric",
            "2 carrots, diced small",
            "Fresh parsley for garnish"
        ],
        "instructions": [
            "Rinse rice until water runs clear. Set aside.",
            "Season chicken with salt and turmeric.",
            "Heat olive oil in a large pot over medium heat.",
            "Cook chicken until golden, about 6 minutes per side. Remove and set aside.",
            "Add rice to the same pot, stir for 2 minutes.",
            "Add broth and bring to boil. Reduce heat and simmer covered for 18 minutes.",
            "Shred chicken and fold back into rice with carrots.",
            "Let rest 5 minutes, then garnish with parsley."
        ],
        "story": "This was the first meal I could eat without discomfort after months of digestive issues. The gentle flavors and easily digestible ingredients made it a cornerstone of my healing journey."
    },
    {
        "id": "2",
        "title": "Healing Bone Broth",
        "description": "Nutrient-rich bone broth that soothes the gut and provides essential minerals.",
        "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&h=400&fit=crop",
        "prep_time": "20 min",
        "cook_time": "12 hours",
        "servings": 8,
        "difficulty": "Easy",
        "dietary_tags": ["gluten-free", "dairy-free", "paleo", "keto"],
        "ingredients": [
            "3 lbs beef or chicken bones",
            "2 tbsp apple cider vinegar",
            "1 onion, quartered",
            "2 celery stalks",
            "2 bay leaves",
            "1 tsp sea salt",
            "12 cups filtered water",
            "Fresh herbs (thyme, rosemary)"
        ],
        "instructions": [
            "Place bones in slow cooker or large pot.",
            "Add vinegar and let sit for 30 minutes.",
            "Add remaining ingredients and cover with water.",
            "Cook on low for 12-24 hours (slow cooker) or simmer gently on stovetop.",
            "Strain through fine mesh strainer.",
            "Cool completely and refrigerate. Remove fat layer when cold.",
            "Reheat portions as needed. Can be frozen for up to 6 months."
        ],
        "story": "Bone broth became my daily ritual. The collagen and minerals helped heal my gut lining, and the warm, comforting liquid was often all I could manage on difficult days."
    },
    {
        "id": "3",
        "title": "Simple Baked Sweet Potato",
        "description": "Perfectly baked sweet potato with gut-friendly toppings.",
        "image": "https://images.unsplash.com/photo-1518788335250-ee7a8b39f0cb?w=600&h=400&fit=crop",
        "prep_time": "5 min",
        "cook_time": "45 min",
        "servings": 1,
        "difficulty": "Easy",
        "dietary_tags": ["gluten-free", "dairy-free", "vegan", "paleo"],
        "ingredients": [
            "1 medium sweet potato",
            "1 tbsp olive oil",
            "1/4 tsp sea salt",
            "1 tbsp coconut oil",
            "Cinnamon to taste",
            "Optional: chopped chives"
        ],
        "instructions": [
            "Preheat oven to 425°F (220°C).",
            "Wash and pierce sweet potato with fork.",
            "Rub with olive oil and salt.",
            "Bake for 45-60 minutes until tender.",
            "Cut open and fluff with fork.",
            "Top with coconut oil, cinnamon, and chives if using."
        ],
        "story": "Sweet potatoes were one of the few foods that never caused me issues. They provided gentle energy and essential nutrients when my diet was very limited."
    },
    {
        "id": "4",
        "title": "Gentle Ginger Tea",
        "description": "Soothing ginger tea to calm digestive discomfort.",
        "image": "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=600&h=400&fit=crop",
        "prep_time": "5 min",
        "cook_time": "10 min",
        "servings": 1,
        "difficulty": "Easy",
        "dietary_tags": ["gluten-free", "dairy-free", "vegan"],
        "ingredients": [
            "1 inch fresh ginger root",
            "1 cup filtered water",
            "1 tsp raw honey (optional)",
            "Lemon slice (optional)"
        ],
        "instructions": [
            "Peel and slice ginger root thinly.",
            "Bring water to boil in small saucepan.",
            "Add ginger slices and reduce heat.",
            "Simmer gently for 8-10 minutes.",
            "Strain into mug.",
            "Add honey and lemon if tolerated."
        ],
        "story": "Ginger tea was my constant companion during flare-ups. The anti-inflammatory properties helped reduce nausea and settle my stomach naturally."
    },
    {
        "id": "5",
        "title": "Quinoa Porridge Bowl",
        "description": "Creamy, nutritious breakfast that is gentle on sensitive stomachs.",
        "image": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?w=600&h=400&fit=crop",
        "prep_time": "5 min",
        "cook_time": "20 min",
        "servings": 2,
        "difficulty": "Easy",
        "dietary_tags": ["gluten-free", "dairy-free", "vegan"],
        "ingredients": [
            "1 cup quinoa, rinsed",
            "2 cups coconut milk",
            "1 cup water",
            "2 tbsp maple syrup",
            "1/2 tsp vanilla extract",
            "1/4 tsp cinnamon",
            "Pinch of salt",
            "Fresh berries for topping"
        ],
        "instructions": [
            "Combine quinoa, coconut milk, and water in saucepan.",
            "Bring to boil, then reduce heat to low.",
            "Simmer covered for 15-20 minutes until creamy.",
            "Stir in maple syrup, vanilla, cinnamon, and salt.",
            "Serve warm topped with fresh berries.",
            "Can be refrigerated and reheated with extra liquid."
        ],
        "story": "When oats were too harsh for my system, quinoa porridge became my go-to breakfast. It provided protein and sustained energy without digestive distress."
    }
]

SEED_PERSONAL_STORY = {
    "id": "main-story",
    "title": "My Healing Journey",
    "subtitle": "From digestive distress to gut-friendly nourishment",
    "content": [
        "Three years ago, I found myself in a place many of you might recognize - struggling with severe digestive issues that left me afraid to eat. What started as occasional discomfort had evolved into daily pain, bloating, and a growing list of foods that seemed to trigger symptoms.",
        "After months of elimination diets, medical consultations, and countless nights researching gut health, I realized that healing would require more than just removing problematic foods. I needed to rebuild my relationship with nourishment entirely.",
        "The recipes you'll find here aren't just meals - they're stepping stones on a healing journey. Each dish was carefully crafted during my recovery, tested not just for taste, but for how gentle they were on my sensitive system. Some became daily staples, others were comfort foods for difficult days.",
        "I'm sharing these recipes because I know how isolating digestive issues can feel, and how overwhelming it can be to figure out what's safe to eat. My hope is that these simple, nourishing meals can provide you with both physical comfort and the reassurance that healing is possible."
    ],
    "image": "https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=600&h=400&fit=crop"
}

async def seed_database():
    """Seed the database with initial data if collections are empty"""
    try:
        # Check if recipes collection is empty
        recipe_count = await db.recipes.count_documents({})
        if recipe_count == 0:
            logger.info("Seeding recipes collection...")
            for recipe_data in SEED_RECIPES:
                recipe = Recipe(**recipe_data)
                await db.recipes.insert_one(recipe.dict())
            logger.info(f"Successfully seeded {len(SEED_RECIPES)} recipes")
        
        # Check if personal story exists
        story_count = await db.personal_stories.count_documents({})
        if story_count == 0:
            logger.info("Seeding personal story...")
            story = PersonalStory(**SEED_PERSONAL_STORY)
            await db.personal_stories.insert_one(story.dict())
            logger.info("Successfully seeded personal story")
            
        # Create indexes for better search performance
        await db.recipes.create_index([("title", "text"), ("description", "text"), ("ingredients", "text")])
        await db.recipes.create_index("dietary_tags")
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")

@app.on_event("startup")
async def startup_event():
    await seed_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# React static file serving - MUST BE AT THE VERY END
if os.path.exists("build"):
    # Serve static files (CSS, JS, images, etc.)
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    
    # Check for other common asset directories
    if os.path.exists("build/assets"):
        app.mount("/assets", StaticFiles(directory="build/assets"), name="assets")
    
    # Serve favicon and manifest files directly from build
    @app.get("/favicon.ico")
    async def favicon():
        return FileResponse("build/favicon.ico")
    
    @app.get("/manifest.json")
    async def manifest():
        return FileResponse("build/manifest.json")
    
    # Catch-all route for React Router - MUST BE LAST
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Don't serve React for API routes
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API route not found")
        
        # Serve React app for all other routes
        return FileResponse("build/index.html")
else:
    # Fallback when build directory doesn't exist
    @app.get("/")
    async def no_build_warning():
        return {
            "message": "React build not found", 
            "instructions": "Run 'npm run build' and ensure the build folder is in the same directory as server.py",
            "api_available": "API is available at /api/"
        }
