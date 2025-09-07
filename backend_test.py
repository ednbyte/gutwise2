#!/usr/bin/env python3
"""
GutWise Recipe API Backend Test Suite
Tests all API endpoints for the GutWise recipe application
"""

import requests
import json
import sys
from typing import Dict, Any, List
import os
from pathlib import Path

# Load environment variables to get the backend URL
def load_env_file(file_path: str) -> Dict[str, str]:
    """Load environment variables from .env file"""
    env_vars = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value.strip('"')
    return env_vars

# Get backend URL from frontend .env file
frontend_env = load_env_file('/app/frontend/.env')
BASE_URL = frontend_env.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BASE_URL}/api"

print(f"Testing GutWise Recipe API at: {API_BASE_URL}")
print("=" * 60)

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str = "", response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
        if response_data and not success:
            print(f"    Response: {response_data}")
        print()
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'response_data': response_data
        })
    
    def test_health_check(self):
        """Test GET /api/ - Health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "GutWise" in data["message"]:
                    self.log_test("Health Check", True, f"Status: {response.status_code}, Message: {data['message']}")
                else:
                    self.log_test("Health Check", False, f"Unexpected response format: {data}")
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
    
    def test_get_all_recipes(self):
        """Test GET /api/recipes - Should return 5 seeded recipes"""
        try:
            response = self.session.get(f"{self.base_url}/recipes")
            if response.status_code == 200:
                recipes = response.json()
                if len(recipes) == 5:
                    # Verify expected recipe titles
                    expected_titles = [
                        "Gentle Chicken and Rice Bowl",
                        "Healing Bone Broth", 
                        "Simple Baked Sweet Potato",
                        "Gentle Ginger Tea",
                        "Quinoa Porridge Bowl"
                    ]
                    actual_titles = [recipe['title'] for recipe in recipes]
                    missing_titles = [title for title in expected_titles if title not in actual_titles]
                    
                    if not missing_titles:
                        self.log_test("Get All Recipes", True, f"Found all 5 expected recipes")
                    else:
                        self.log_test("Get All Recipes", False, f"Missing recipes: {missing_titles}")
                else:
                    self.log_test("Get All Recipes", False, f"Expected 5 recipes, got {len(recipes)}")
            else:
                self.log_test("Get All Recipes", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get All Recipes", False, f"Exception: {str(e)}")
    
    def test_search_recipes(self):
        """Test GET /api/recipes?search=chicken - Search functionality"""
        try:
            response = self.session.get(f"{self.base_url}/recipes?search=chicken")
            if response.status_code == 200:
                recipes = response.json()
                if len(recipes) >= 1:
                    # Check if chicken recipe is found
                    chicken_found = any("chicken" in recipe['title'].lower() or 
                                      "chicken" in recipe['description'].lower() or
                                      any("chicken" in ingredient.lower() for ingredient in recipe['ingredients'])
                                      for recipe in recipes)
                    if chicken_found:
                        self.log_test("Search Recipes (chicken)", True, f"Found {len(recipes)} recipe(s) containing 'chicken'")
                    else:
                        self.log_test("Search Recipes (chicken)", False, "No recipes containing 'chicken' found")
                else:
                    self.log_test("Search Recipes (chicken)", False, "No recipes found for 'chicken' search")
            else:
                self.log_test("Search Recipes (chicken)", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Search Recipes (chicken)", False, f"Exception: {str(e)}")
    
    def test_filter_single_dietary_tag(self):
        """Test GET /api/recipes?dietary_tags=gluten-free - Filter by single dietary tag"""
        try:
            response = self.session.get(f"{self.base_url}/recipes?dietary_tags=gluten-free")
            if response.status_code == 200:
                recipes = response.json()
                if len(recipes) == 5:  # All 5 recipes should be gluten-free
                    # Verify all recipes have gluten-free tag
                    all_gluten_free = all("gluten-free" in recipe['dietary_tags'] for recipe in recipes)
                    if all_gluten_free:
                        self.log_test("Filter Single Dietary Tag (gluten-free)", True, f"Found {len(recipes)} gluten-free recipes")
                    else:
                        self.log_test("Filter Single Dietary Tag (gluten-free)", False, "Some recipes don't have gluten-free tag")
                else:
                    self.log_test("Filter Single Dietary Tag (gluten-free)", False, f"Expected 5 gluten-free recipes, got {len(recipes)}")
            else:
                self.log_test("Filter Single Dietary Tag (gluten-free)", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Filter Single Dietary Tag (gluten-free)", False, f"Exception: {str(e)}")
    
    def test_filter_multiple_dietary_tags(self):
        """Test GET /api/recipes?dietary_tags=gluten-free,dairy-free - Filter by multiple dietary tags"""
        try:
            response = self.session.get(f"{self.base_url}/recipes?dietary_tags=gluten-free,dairy-free")
            if response.status_code == 200:
                recipes = response.json()
                if len(recipes) == 5:  # All 5 recipes should be both gluten-free and dairy-free
                    # Verify all recipes have both tags
                    all_match = all("gluten-free" in recipe['dietary_tags'] and 
                                  "dairy-free" in recipe['dietary_tags'] 
                                  for recipe in recipes)
                    if all_match:
                        self.log_test("Filter Multiple Dietary Tags (gluten-free,dairy-free)", True, f"Found {len(recipes)} recipes with both tags")
                    else:
                        self.log_test("Filter Multiple Dietary Tags (gluten-free,dairy-free)", False, "Some recipes don't have both required tags")
                else:
                    self.log_test("Filter Multiple Dietary Tags (gluten-free,dairy-free)", False, f"Expected 5 recipes with both tags, got {len(recipes)}")
            else:
                self.log_test("Filter Multiple Dietary Tags (gluten-free,dairy-free)", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Filter Multiple Dietary Tags (gluten-free,dairy-free)", False, f"Exception: {str(e)}")
    
    def test_pagination(self):
        """Test GET /api/recipes?limit=2 - Pagination test"""
        try:
            response = self.session.get(f"{self.base_url}/recipes?limit=2")
            if response.status_code == 200:
                recipes = response.json()
                if len(recipes) == 2:
                    self.log_test("Pagination (limit=2)", True, f"Successfully limited results to {len(recipes)} recipes")
                else:
                    self.log_test("Pagination (limit=2)", False, f"Expected 2 recipes, got {len(recipes)}")
            else:
                self.log_test("Pagination (limit=2)", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Pagination (limit=2)", False, f"Exception: {str(e)}")
    
    def test_get_specific_recipe(self):
        """Test GET /api/recipes/{id} - Get specific recipe with id "1" """
        try:
            response = self.session.get(f"{self.base_url}/recipes/1")
            if response.status_code == 200:
                recipe = response.json()
                if recipe['id'] == "1" and recipe['title'] == "Gentle Chicken and Rice Bowl":
                    self.log_test("Get Specific Recipe (id=1)", True, f"Found recipe: {recipe['title']}")
                else:
                    self.log_test("Get Specific Recipe (id=1)", False, f"Unexpected recipe data: {recipe}")
            else:
                self.log_test("Get Specific Recipe (id=1)", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Specific Recipe (id=1)", False, f"Exception: {str(e)}")
    
    def test_get_specific_recipe_not_found(self):
        """Test GET /api/recipes/{id} - Test error handling for invalid ID"""
        try:
            response = self.session.get(f"{self.base_url}/recipes/invalid-id")
            if response.status_code == 404:
                self.log_test("Get Specific Recipe (invalid ID)", True, "Correctly returned 404 for invalid recipe ID")
            else:
                self.log_test("Get Specific Recipe (invalid ID)", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Get Specific Recipe (invalid ID)", False, f"Exception: {str(e)}")
    
    def test_get_dietary_filters(self):
        """Test GET /api/dietary-filters - Get dietary filters with counts"""
        try:
            response = self.session.get(f"{self.base_url}/dietary-filters")
            if response.status_code == 200:
                filters = response.json()
                
                # Expected counts based on seeded data
                expected_counts = {
                    "gluten-free": 5,
                    "dairy-free": 5,
                    "low-fodmap": 1,
                    "vegan": 3,
                    "paleo": 2,
                    "keto": 1
                }
                
                # Convert to dict for easier checking
                actual_counts = {f['id']: f['count'] for f in filters}
                
                all_correct = True
                for tag, expected_count in expected_counts.items():
                    if tag not in actual_counts:
                        self.log_test("Get Dietary Filters", False, f"Missing dietary tag: {tag}")
                        all_correct = False
                    elif actual_counts[tag] != expected_count:
                        self.log_test("Get Dietary Filters", False, f"Wrong count for {tag}: expected {expected_count}, got {actual_counts[tag]}")
                        all_correct = False
                
                if all_correct:
                    self.log_test("Get Dietary Filters", True, f"All dietary filter counts are correct")
                
            else:
                self.log_test("Get Dietary Filters", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Dietary Filters", False, f"Exception: {str(e)}")
    
    def test_get_personal_story(self):
        """Test GET /api/personal-story - Get personal story"""
        try:
            response = self.session.get(f"{self.base_url}/personal-story")
            if response.status_code == 200:
                story = response.json()
                if (story['title'] == "My Healing Journey" and 
                    story['subtitle'] == "From digestive distress to gut-friendly nourishment" and
                    len(story['content']) == 4):
                    self.log_test("Get Personal Story", True, f"Personal story found: {story['title']}")
                else:
                    self.log_test("Get Personal Story", False, f"Unexpected story data: {story}")
            else:
                self.log_test("Get Personal Story", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Personal Story", False, f"Exception: {str(e)}")
    
    def test_create_recipe(self):
        """Test POST /api/recipes - Create new recipe"""
        try:
            new_recipe = {
                "title": "Test Healing Smoothie",
                "description": "A gentle smoothie for sensitive stomachs",
                "image": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&h=400&fit=crop",
                "prep_time": "5 min",
                "cook_time": "0 min",
                "servings": 1,
                "difficulty": "Easy",
                "dietary_tags": ["gluten-free", "dairy-free", "vegan"],
                "ingredients": [
                    "1 banana",
                    "1 cup coconut milk",
                    "1 tbsp almond butter",
                    "1 tsp vanilla extract"
                ],
                "instructions": [
                    "Add all ingredients to blender",
                    "Blend until smooth",
                    "Serve immediately"
                ],
                "story": "This smoothie was created during testing to verify the API functionality."
            }
            
            response = self.session.post(
                f"{self.base_url}/recipes",
                json=new_recipe,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                created_recipe = response.json()
                if (created_recipe['title'] == new_recipe['title'] and 
                    'id' in created_recipe and
                    created_recipe['dietary_tags'] == new_recipe['dietary_tags']):
                    self.log_test("Create Recipe", True, f"Successfully created recipe: {created_recipe['title']}")
                    
                    # Verify the recipe was actually saved by fetching it
                    get_response = self.session.get(f"{self.base_url}/recipes/{created_recipe['id']}")
                    if get_response.status_code == 200:
                        self.log_test("Verify Created Recipe", True, "Created recipe can be retrieved")
                    else:
                        self.log_test("Verify Created Recipe", False, "Created recipe cannot be retrieved")
                else:
                    self.log_test("Create Recipe", False, f"Unexpected response data: {created_recipe}")
            else:
                self.log_test("Create Recipe", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Create Recipe", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("Starting GutWise Recipe API Tests...")
        print()
        
        # Run all tests
        self.test_health_check()
        self.test_get_all_recipes()
        self.test_search_recipes()
        self.test_filter_single_dietary_tag()
        self.test_filter_multiple_dietary_tags()
        self.test_pagination()
        self.test_get_specific_recipe()
        self.test_get_specific_recipe_not_found()
        self.test_get_dietary_filters()
        self.test_get_personal_story()
        self.test_create_recipe()
        
        # Summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"❌ {result['test']}: {result['message']}")
        
        return failed_tests == 0

if __name__ == "__main__":
    tester = APITester(API_BASE_URL)
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)