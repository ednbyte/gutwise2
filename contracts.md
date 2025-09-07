# API Contracts & Backend Implementation Plan

## Overview
This document outlines the API contracts, data models, and integration plan for the GutWise recipe website backend implementation.

## Data Models

### Recipe Model
```python
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
```

### PersonalStory Model
```python
class PersonalStory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    content: List[str]  # Array of paragraphs
    image: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## API Endpoints

### Recipe Endpoints
- `GET /api/recipes` - Get all recipes with optional filters
  - Query params: `search`, `dietary_tags`, `limit`, `offset`
  - Returns: `List[Recipe]`

- `GET /api/recipes/{recipe_id}` - Get single recipe by ID
  - Returns: `Recipe`

- `POST /api/recipes` - Create new recipe (admin functionality)
  - Body: `RecipeCreate`
  - Returns: `Recipe`

- `PUT /api/recipes/{recipe_id}` - Update recipe (admin functionality)
  - Body: `RecipeUpdate`
  - Returns: `Recipe`

- `DELETE /api/recipes/{recipe_id}` - Delete recipe (admin functionality)
  - Returns: `{"message": "Recipe deleted"}`

### Dietary Filter Endpoints
- `GET /api/dietary-filters` - Get all dietary filters with counts
  - Returns: `List[DietaryFilter]`

### Personal Story Endpoints
- `GET /api/personal-story` - Get the main personal story
  - Returns: `PersonalStory`

- `PUT /api/personal-story` - Update personal story (admin functionality)
  - Body: `PersonalStoryUpdate`
  - Returns: `PersonalStory`

## Mock Data Migration
Current mock data in `/frontend/src/mock.js` includes:

### mockRecipes (5 recipes):
1. Gentle Chicken and Rice Bowl
2. Healing Bone Broth  
3. Simple Baked Sweet Potato
4. Gentle Ginger Tea
5. Quinoa Porridge Bowl

### dietaryFilters:
- gluten-free (5 recipes)
- dairy-free (5 recipes)  
- low-fodmap (1 recipe)
- vegan (3 recipes)
- paleo (2 recipes)
- keto (1 recipe)

### personalStory:
- Title, subtitle, content array, and image

## Backend Implementation Tasks

1. **Database Setup**
   - Create Recipe collection in MongoDB
   - Create PersonalStory collection in MongoDB
   - Add indexes for search optimization

2. **Data Models**
   - Implement Pydantic models for Recipe, PersonalStory
   - Add validation and serialization

3. **API Endpoints**
   - Implement all CRUD operations for recipes
   - Add search functionality (text search on title, description, ingredients)
   - Add filtering by dietary tags
   - Implement dietary filter counts aggregation
   - Personal story management

4. **Data Migration**
   - Create script to populate database with mock data
   - Ensure all current mock recipes are preserved

5. **Search & Filter Logic**
   - Text search across title, description, and ingredients
   - Multiple dietary tag filtering (AND operation)
   - Dynamic filter counts based on current search results

## Frontend Integration Changes

### Files to Update:
1. **Remove mock.js** - Delete the mock data file
2. **Update HomePage.js** - Replace mock data calls with API calls
3. **Update RecipesPage.js** - Replace mock data and add API integration for search/filter
4. **Update RecipeDetail.js** - Replace mock data with API call
5. **Add API service layer** - Create `services/api.js` for centralized API calls

### API Integration Points:
- Homepage: `GET /api/recipes?limit=3` for featured recipes
- Homepage: `GET /api/personal-story` for story section
- Recipes Page: `GET /api/recipes` with search and filter params
- Recipes Page: `GET /api/dietary-filters` for filter options
- Recipe Detail: `GET /api/recipes/{id}` for individual recipe

### Error Handling:
- Add loading states for all API calls
- Add error states for failed requests
- Add retry mechanisms for network failures
- Add fallback UI for missing data

## Database Seeding Strategy
1. Check if recipes collection is empty on startup
2. If empty, seed with mock data automatically
3. Ensure personal story is created
4. Log successful seeding

## Testing Requirements
- All endpoints should return proper HTTP status codes
- Search functionality should work with partial matches
- Filter functionality should support multiple tags
- Recipe CRUD operations should work correctly
- Data validation should prevent invalid entries

## Performance Considerations
- Add database indexes for search fields
- Implement pagination for recipe listings
- Cache dietary filter counts
- Optimize image loading and storage