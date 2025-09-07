from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
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
client = AsyncIOMotorClient(mongo_url)
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
