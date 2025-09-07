import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Clock, Users, Heart } from 'lucide-react';
import { recipeApi, personalStoryApi } from '../services/api';

const HomePage = () => {
  const [featuredRecipes, setFeaturedRecipes] = useState([]);
  const [personalStory, setPersonalStory] = useState(null);
  const [totalRecipes, setTotalRecipes] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch featured recipes (first 3)
        const recipes = await recipeApi.getRecipes({ limit: 3 });
        setFeaturedRecipes(recipes);

        // Fetch all recipes count
        const allRecipes = await recipeApi.getRecipes();
        setTotalRecipes(allRecipes.length);

        // Fetch personal story
        const story = await personalStoryApi.getPersonalStory();
        setPersonalStory(story);

      } catch (err) {
        setError('Failed to load content. Please try again later.');
        console.error('Error fetching homepage data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading nourishing content...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-green-50 to-blue-50 py-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Gut-Friendly Recipes for
              <span className="text-green-600 block">Healing & Nourishment</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              Discover gentle, delicious recipes that support digestive health. 
              Each dish has been carefully crafted and tested during my own healing journey.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/recipes"
                className="bg-green-600 text-white px-8 py-4 rounded-lg font-semibold 
                         hover:bg-green-700 transition-all duration-200 transform hover:scale-105
                         shadow-lg hover:shadow-xl flex items-center justify-center group"
              >
                Browse Recipes
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <a
                href="#story"
                className="border-2 border-green-600 text-green-600 px-8 py-4 rounded-lg font-semibold
                         hover:bg-green-600 hover:text-white transition-all duration-200
                         flex items-center justify-center"
              >
                Read My Story
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center 
                            justify-center mx-auto mb-4">
                <Heart className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {totalRecipes}+ Recipes
              </h3>
              <p className="text-gray-600">Carefully tested gut-friendly meals</p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center 
                            justify-center mx-auto mb-4">
                <Clock className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Quick & Easy</h3>
              <p className="text-gray-600">Most recipes under 30 minutes</p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center 
                            justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Community Tested</h3>
              <p className="text-gray-600">Loved by those with food sensitivities</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Recipes */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Featured Recipes</h2>
            <p className="text-lg text-gray-600">Start your healing journey with these gentle, nourishing meals</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {featuredRecipes.map((recipe) => (
              <Link
                key={recipe.id}
                to={`/recipe/${recipe.id}`}
                className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300
                         transform hover:-translate-y-2 overflow-hidden group"
              >
                <div className="aspect-w-16 aspect-h-9 overflow-hidden">
                  <img
                    src={recipe.image}
                    alt={recipe.title}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="p-6">
                  <div className="flex flex-wrap gap-2 mb-3">
                    {recipe.dietary_tags.slice(0, 2).map((tag) => (
                      <span
                        key={tag}
                        className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-medium"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-green-600 transition-colors">
                    {recipe.title}
                  </h3>
                  <p className="text-gray-600 mb-4 line-clamp-2">
                    {recipe.description}
                  </p>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>{recipe.prep_time}</span>
                    <span>{recipe.servings} servings</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Link
              to="/recipes"
              className="inline-flex items-center bg-green-600 text-white px-8 py-3 rounded-lg
                       font-semibold hover:bg-green-700 transition-colors duration-200 group"
            >
              View All Recipes
              <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>

      {/* Personal Story Section */}
      {personalStory && (
        <section id="story" className="py-20 bg-white">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">{personalStory.title}</h2>
              <p className="text-xl text-gray-600">{personalStory.subtitle}</p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div className="space-y-6">
                {personalStory.content.map((paragraph, index) => (
                  <p key={index} className="text-gray-700 leading-relaxed">
                    {paragraph}
                  </p>
                ))}
              </div>
              
              <div className="relative">
                <div className="aspect-w-4 aspect-h-3 rounded-xl overflow-hidden shadow-lg">
                  <img
                    src={personalStory.image}
                    alt="Healing foods"
                    className="w-full h-80 object-cover"
                  />
                </div>
                <div className="absolute -bottom-6 -right-6 bg-green-600 text-white p-4 rounded-xl shadow-lg">
                  <Heart className="h-8 w-8" />
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-green-600 to-blue-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Start Your Healing Journey?
          </h2>
          <p className="text-xl text-green-100 mb-8">
            Join thousands who have found comfort and nourishment through these gentle recipes.
          </p>
          <Link
            to="/recipes"
            className="bg-white text-green-600 px-8 py-4 rounded-lg font-semibold
                     hover:bg-gray-100 transition-colors duration-200 inline-flex items-center group"
          >
            Explore Recipes Now
            <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;