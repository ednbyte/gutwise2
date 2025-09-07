import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Clock, Users, ChefHat, Heart } from 'lucide-react';
import { mockRecipes } from '../mock';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Separator } from '../components/ui/separator';

const RecipeDetail = () => {
  const { id } = useParams();
  const recipe = mockRecipes.find(r => r.id === id);

  if (!recipe) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Recipe Not Found</h1>
          <Link to="/recipes">
            <Button>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Recipes
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="relative h-96 overflow-hidden">
        <img 
          src={recipe.image} 
          alt={recipe.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
        <div className="absolute inset-0 flex items-end">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-8 w-full">
            <Link to="/recipes" className="inline-flex items-center text-white mb-4 hover:text-green-200 transition-colors">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Recipes
            </Link>
            <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              {recipe.title}
            </h1>
            <p className="text-xl text-gray-200 max-w-2xl">
              {recipe.description}
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Recipe Info Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4 text-center">
                  <Clock className="h-6 w-6 text-green-600 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Prep Time</div>
                  <div className="font-semibold">{recipe.prepTime}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="p-4 text-center">
                  <ChefHat className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Cook Time</div>
                  <div className="font-semibold">{recipe.cookTime}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="p-4 text-center">
                  <Users className="h-6 w-6 text-purple-600 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Servings</div>
                  <div className="font-semibold">{recipe.servings}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="p-4 text-center">
                  <Heart className="h-6 w-6 text-red-500 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Difficulty</div>
                  <div className="font-semibold">{recipe.difficulty}</div>
                </CardContent>
              </Card>
            </div>

            {/* Dietary Tags */}
            <Card>
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold mb-4">Dietary Information</h3>
                <div className="flex flex-wrap gap-2">
                  {recipe.dietaryTags.map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-sm">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Personal Story */}
            {recipe.story && (
              <Card className="bg-green-50 border-green-200">
                <CardHeader>
                  <CardTitle className="text-green-800 flex items-center">
                    <Heart className="mr-2 h-5 w-5" />
                    My Story with This Recipe
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-green-700 italic leading-relaxed">
                    "{recipe.story}"
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Instructions */}
            <Card>
              <CardHeader>
                <CardTitle>Instructions</CardTitle>
              </CardHeader>
              <CardContent>
                <ol className="space-y-4">
                  {recipe.instructions.map((instruction, index) => (
                    <li key={index} className="flex">
                      <span className="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full 
                                     flex items-center justify-center text-sm font-semibold mr-4 mt-0.5">
                        {index + 1}
                      </span>
                      <p className="text-gray-700 leading-relaxed">{instruction}</p>
                    </li>
                  ))}
                </ol>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Ingredients */}
            <Card className="sticky top-24">
              <CardHeader>
                <CardTitle>Ingredients</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {recipe.ingredients.map((ingredient, index) => (
                    <li key={index} className="flex items-start">
                      <span className="w-2 h-2 bg-green-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span className="text-gray-700">{ingredient}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {/* Call to Action */}
            <Card className="bg-gradient-to-br from-green-50 to-blue-50 border-green-200">
              <CardContent className="p-6 text-center">
                <Heart className="h-12 w-12 text-green-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Love this recipe?
                </h3>
                <p className="text-gray-600 mb-4 text-sm">
                  Discover more gut-friendly meals that support your healing journey
                </p>
                <Link to="/recipes">
                  <Button className="w-full">
                    Explore More Recipes
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetail;