import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Recipe API methods
export const recipeApi = {
  // Get all recipes with optional search and filters
  getRecipes: async (params = {}) => {
    try {
      const response = await apiClient.get('/recipes', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching recipes:', error);
      throw error;
    }
  },

  // Get single recipe by ID
  getRecipe: async (id) => {
    try {
      const response = await apiClient.get(`/recipes/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching recipe ${id}:`, error);
      throw error;
    }
  },

  // Create new recipe (admin functionality)
  createRecipe: async (recipeData) => {
    try {
      const response = await apiClient.post('/recipes', recipeData);
      return response.data;
    } catch (error) {
      console.error('Error creating recipe:', error);
      throw error;
    }
  },

  // Get dietary filters with counts
  getDietaryFilters: async () => {
    try {
      const response = await apiClient.get('/dietary-filters');
      return response.data;
    } catch (error) {
      console.error('Error fetching dietary filters:', error);
      throw error;
    }
  },
};

// Personal story API methods
export const personalStoryApi = {
  // Get the main personal story
  getPersonalStory: async () => {
    try {
      const response = await apiClient.get('/personal-story');
      return response.data;
    } catch (error) {
      console.error('Error fetching personal story:', error);
      throw error;
    }
  },
};

// Health check
export const healthApi = {
  checkHealth: async () => {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      console.error('Error checking API health:', error);
      throw error;
    }
  },
};

export default {
  recipeApi,
  personalStoryApi,
  healthApi,
};