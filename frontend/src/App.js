import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Input } from './components/ui/input';
import { Badge } from './components/ui/badge';
import { MapPin, ShoppingCart, ChefHat, DollarSign, Clock, Users } from 'lucide-react';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [userLocation, setUserLocation] = useState(null);
  const [nearbyStores, setNearbyStores] = useState([]);
  const [selectedStore, setSelectedStore] = useState(null);
  const [saleItems, setSaleItems] = useState([]);
  const [generatedRecipes, setGeneratedRecipes] = useState([]);
  const [selectedRecipes, setSelectedRecipes] = useState([]);
  const [groceryList, setGroceryList] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState('location');

  // Get user location
  const getCurrentLocation = () => {
    setLoading(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          setUserLocation(location);
          await findNearbyStores(location);
          setCurrentStep('stores');
          setLoading(false);
          toast.success('Location found! Searching for nearby stores...');
        },
        (error) => {
          console.error('Error getting location:', error);
          // Fallback to Toronto coordinates for demo
          const fallbackLocation = { latitude: 43.6532, longitude: -79.3832 };
          setUserLocation(fallbackLocation);
          findNearbyStores(fallbackLocation);
          setCurrentStep('stores');
          setLoading(false);
          toast.info('Using default location (Toronto) for demo');
        }
      );
    } else {
      const fallbackLocation = { latitude: 43.6532, longitude: -79.3832 };
      setUserLocation(fallbackLocation);
      findNearbyStores(fallbackLocation);
      setCurrentStep('stores');
      setLoading(false);
      toast.info('Geolocation not supported. Using Toronto for demo');
    }
  };

  // Find nearby stores
  const findNearbyStores = async (location) => {
    try {
      const response = await axios.post(`${API}/stores/nearby`, location);
      setNearbyStores(response.data);
      if (response.data.length > 0) {
        const firstStore = response.data[0];
        setSelectedStore(firstStore);
        await getStoreSales(firstStore.id);
      }
    } catch (error) {
      console.error('Error finding stores:', error);
      toast.error('Error finding nearby stores');
    }
  };

  // Get store sales
  const getStoreSales = async (storeId) => {
    try {
      const response = await axios.get(`${API}/stores/${storeId}/sales`);
      setSaleItems(response.data);
      setCurrentStep('sales');
    } catch (error) {
      console.error('Error getting sales:', error);
      toast.error('Error loading store sales');
    }
  };

  // Generate recipes based on sale items
  const generateRecipes = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/recipes/generate`, {
        sale_items: saleItems,
        dietary_preferences: [],
        servings: 4
      });
      setGeneratedRecipes(response.data);
      setCurrentStep('recipes');
      toast.success('Recipes generated based on current sales!');
    } catch (error) {
      console.error('Error generating recipes:', error);
      toast.error('Error generating recipes. Please try again.');
    }
    setLoading(false);
  };

  // Generate grocery list
  const generateGroceryList = async () => {
    if (selectedRecipes.length === 0) {
      toast.error('Please select at least one recipe');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/grocery-list/generate`, {
        user_location: userLocation,
        selected_recipes: selectedRecipes,
        servings_multiplier: 1.0
      });
      setGroceryList(response.data);
      setCurrentStep('groceryList');
      toast.success('Grocery list generated!');
    } catch (error) {
      console.error('Error generating grocery list:', error);
      toast.error('Error generating grocery list');
    }
    setLoading(false);
  };

  // Toggle recipe selection
  const toggleRecipeSelection = (recipeId) => {
    setSelectedRecipes(prev => 
      prev.includes(recipeId) 
        ? prev.filter(id => id !== recipeId)
        : [...prev, recipeId]
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Hero Section */}
      <div className="relative bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl" style={{fontFamily: 'Inter, sans-serif'}}>
              <span className="text-green-600">Good</span>Basket
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              Your smart grocery companion - Find the best deals, generate meal plans, and save money on groceries with AI-powered recommendations
            </p>
            <div className="mt-8">
              <img 
                src="https://images.unsplash.com/photo-1693505628207-dbeb3d882c92?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxncm9jZXJ5JTIwc2F2aW5nc3xlbnwwfHx8fDE3NTkyNTY4Mjh8MA&ixlib=rb-4.1.0&q=85" 
                alt="Grocery Shopping" 
                className="mx-auto h-64 w-full max-w-lg object-cover rounded-lg shadow-lg"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Step Indicator */}
        <div className="flex justify-center mb-8">
          <div className="flex space-x-4">
            {[
              { key: 'location', label: 'Location', icon: MapPin },
              { key: 'stores', label: 'Stores', icon: ShoppingCart },
              { key: 'sales', label: 'Sales', icon: DollarSign },
              { key: 'recipes', label: 'Recipes', icon: ChefHat },
              { key: 'groceryList', label: 'List', icon: ShoppingCart }
            ].map(({ key, label, icon: Icon }) => (
              <div key={key} className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
                currentStep === key ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
              }`}>
                <Icon className="h-4 w-4" />
                <span className="text-sm font-medium">{label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Location Step */}
        {currentStep === 'location' && (
          <Card className="max-w-md mx-auto" data-testid="location-card">
            <CardHeader>
              <CardTitle className="text-center">Find Stores Near You</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-gray-600 mb-4">
                We'll find grocery stores within 25km of your location to show you the best deals
              </p>
              <Button 
                onClick={getCurrentLocation} 
                disabled={loading}
                className="w-full"
                data-testid="get-location-btn"
              >
                {loading ? 'Finding Location...' : 'Get My Location'}
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Stores Step */}
        {currentStep === 'stores' && nearbyStores.length > 0 && (
          <div data-testid="stores-section">
            <h2 className="text-2xl font-bold text-center mb-6">Nearby Grocery Stores</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
              {nearbyStores.slice(0, 6).map((store) => (
                <Card 
                  key={store.id} 
                  className={`cursor-pointer transition-all ${
                    selectedStore?.id === store.id ? 'ring-2 ring-green-500 bg-green-50' : 'hover:shadow-md'
                  }`}
                  onClick={() => setSelectedStore(store)}
                  data-testid={`store-card-${store.chain.toLowerCase()}`}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start space-x-3">
                      <img 
                        src="https://images.unsplash.com/photo-1577745893556-e3d84603c572?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwzfHxncm9jZXJ5JTIwc2F2aW5nc3xlbnwwfHx8fDE3NTkyNTY4Mjh8MA&ixlib=rb-4.1.0&q=85"
                        alt={store.name}
                        className="h-12 w-12 rounded-lg object-cover"
                      />
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{store.name}</h3>
                        <p className="text-sm text-gray-600">{store.chain}</p>
                        <p className="text-xs text-gray-500 mt-1">{store.address}</p>
                        <Badge variant="secondary" className="mt-2">
                          {store.distance_km} km away
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
            {selectedStore && (
              <div className="text-center">
                <Button 
                  onClick={() => getStoreSales(selectedStore.id)}
                  data-testid="view-sales-btn"
                >
                  View {selectedStore.name} Sales
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Sales Step */}
        {currentStep === 'sales' && saleItems.length > 0 && (
          <div data-testid="sales-section">
            <h2 className="text-2xl font-bold text-center mb-6">
              Current Sales at {selectedStore?.name}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
              {saleItems.map((item) => (
                <Card key={item.id} data-testid={`sale-item-${item.name.toLowerCase().replace(/\s+/g, '-')}`}>
                  <CardContent className="p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-gray-900">{item.name}</h3>
                      <Badge variant="destructive">{item.discount_percentage}% OFF</Badge>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-lg font-bold text-green-600">
                        ${item.sale_price.toFixed(2)}
                      </span>
                      <span className="text-sm text-gray-500 line-through">
                        ${item.original_price.toFixed(2)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{item.category}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
            <div className="text-center">
              <Button 
                onClick={generateRecipes} 
                disabled={loading}
                data-testid="generate-recipes-btn"
              >
                {loading ? 'Generating Recipes...' : 'Generate Meal Ideas'}
              </Button>
            </div>
          </div>
        )}

        {/* Recipes Step */}
        {currentStep === 'recipes' && generatedRecipes.length > 0 && (
          <div data-testid="recipes-section">
            <h2 className="text-2xl font-bold text-center mb-6">
              AI-Generated Recipes Using Sale Ingredients
            </h2>
            <div className="grid lg:grid-cols-2 gap-6 mb-8">
              {generatedRecipes.map((recipe) => (
                <Card 
                  key={recipe.id} 
                  className={`cursor-pointer transition-all ${
                    selectedRecipes.includes(recipe.id) ? 'ring-2 ring-green-500 bg-green-50' : 'hover:shadow-md'
                  }`}
                  onClick={() => toggleRecipeSelection(recipe.id)}
                  data-testid={`recipe-card-${recipe.name.toLowerCase().replace(/\s+/g, '-')}`}
                >
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{recipe.name}</CardTitle>
                      {selectedRecipes.includes(recipe.id) && (
                        <Badge className="bg-green-500">Selected</Badge>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4">{recipe.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500 mb-4">
                      <div className="flex items-center">
                        <Clock className="h-4 w-4 mr-1" />
                        {recipe.prep_time + recipe.cook_time} min
                      </div>
                      <div className="flex items-center">
                        <Users className="h-4 w-4 mr-1" />
                        {recipe.servings} servings
                      </div>
                      <div className="flex items-center">
                        <DollarSign className="h-4 w-4 mr-1" />
                        ${recipe.estimated_cost.toFixed(2)}
                      </div>
                    </div>
                    {recipe.dietary_tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-4">
                        {recipe.dietary_tags.map((tag) => (
                          <Badge key={tag} variant="outline" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    )}
                    <div className="text-sm">
                      <p className="font-medium mb-1">Key Ingredients:</p>
                      <ul className="text-gray-600">
                        {recipe.ingredients.slice(0, 3).map((ing, idx) => (
                          <li key={idx}>• {ing.name} ({ing.quantity} {ing.unit})</li>
                        ))}
                        {recipe.ingredients.length > 3 && <li>• ...and more</li>}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
            <div className="text-center">
              <p className="text-gray-600 mb-4">
                Selected {selectedRecipes.length} recipe{selectedRecipes.length !== 1 ? 's' : ''}
              </p>
              <Button 
                onClick={generateGroceryList} 
                disabled={loading || selectedRecipes.length === 0}
                data-testid="generate-grocery-list-btn"
              >
                {loading ? 'Creating List...' : 'Create Grocery List'}
              </Button>
            </div>
          </div>
        )}

        {/* Grocery List Step */}
        {currentStep === 'groceryList' && groceryList && (
          <div data-testid="grocery-list-section">
            <h2 className="text-2xl font-bold text-center mb-6">Your Optimized Grocery List</h2>
            
            {/* Summary */}
            <Card className="mb-6">
              <CardContent className="p-6">
                <div className="grid md:grid-cols-3 gap-4 text-center">
                  <div>
                    <p className="text-2xl font-bold text-green-600">${groceryList.total_cost.toFixed(2)}</p>
                    <p className="text-sm text-gray-600">Total Cost</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-red-600">${groceryList.total_savings.toFixed(2)}</p>
                    <p className="text-sm text-gray-600">You Save</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-blue-600">{groceryList.items.length}</p>
                    <p className="text-sm text-gray-600">Items</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Grocery Items */}
            <div className="grid gap-3">
              {groceryList.items.map((item, idx) => (
                <Card key={idx} data-testid={`grocery-item-${idx}`}>
                  <CardContent className="p-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <h3 className="font-semibold">{item.ingredient}</h3>
                        <p className="text-sm text-gray-600">
                          {item.quantity} from {item.store_name}
                        </p>
                      </div>
                      <div className="text-right">
                        {item.is_on_sale ? (
                          <div>
                            <span className="text-lg font-bold text-green-600">
                              ${item.sale_price?.toFixed(2)}
                            </span>
                            <span className="text-sm text-gray-500 line-through ml-2">
                              ${item.price.toFixed(2)}
                            </span>
                            <Badge variant="destructive" className="ml-2">SALE</Badge>
                          </div>
                        ) : (
                          <span className="text-lg font-semibold">
                            ${item.price.toFixed(2)}
                          </span>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            <div className="text-center mt-8">
              <Button 
                onClick={() => {
                  setCurrentStep('location');
                  setSelectedRecipes([]);
                  setGeneratedRecipes([]);
                  setGroceryList(null);
                }}
                variant="outline"
                data-testid="start-over-btn"
              >
                Start Over
              </Button>
            </div>
          </div>
        )}
      </div>

      <Toaster position="bottom-right" />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
