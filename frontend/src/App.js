import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Input } from './components/ui/input';
import { Badge } from './components/ui/badge';
import { Label } from './components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Checkbox } from './components/ui/checkbox';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog';
import { MapPin, ShoppingCart, ChefHat, DollarSign, Clock, Users, User, Settings, ExternalLink } from 'lucide-react';
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
  const [showProfile, setShowProfile] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const [emailAddress, setEmailAddress] = useState('');
  const [emailLoading, setEmailLoading] = useState(false);

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
          // Only auto-advance to stores if we're still on location step
          if (currentStep === 'location') {
            setCurrentStep('stores');
          }
          setLoading(false);
          toast.success('Location found! Searching for nearby stores...');
        },
        (error) => {
          console.error('Error getting location:', error);
          // Fallback to Toronto coordinates for demo
          const fallbackLocation = { latitude: 43.6532, longitude: -79.3832 };
          setUserLocation(fallbackLocation);
          findNearbyStores(fallbackLocation);
          // Only auto-advance to stores if we're still on location step
          if (currentStep === 'location') {
            setCurrentStep('stores');
          }
          setLoading(false);
          toast.info('Using default location (Toronto) for demo');
        }
      );
    } else {
      const fallbackLocation = { latitude: 43.6532, longitude: -79.3832 };
      setUserLocation(fallbackLocation);
      findNearbyStores(fallbackLocation);
      // Only auto-advance to stores if we're still on location step
      if (currentStep === 'location') {
        setCurrentStep('stores');
      }
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
        // Remove automatic progression - let user click to view sales
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
        dietary_preferences: userProfile?.dietary_preferences || [],
        servings: userProfile?.household_size || 4,
        profile_id: userProfile?.id
      });
      setGeneratedRecipes(response.data);
      setCurrentStep('recipes');
      toast.success('Recipes generated based on current sales and your preferences!');
    } catch (error) {
      console.error('Error generating recipes:', error);
      toast.error('Error generating recipes. Please try again.');
    }
    setLoading(false);
  };

  // Profile management functions
  const saveProfile = async (profileData) => {
    try {
      if (userProfile && userProfile.id) {
        // Update existing profile
        const response = await axios.put(`${API}/profile/${userProfile.id}`, profileData);
        setUserProfile(response.data);
        // Update email field if profile has email
        if (response.data.email && !emailAddress) {
          setEmailAddress(response.data.email);
        }
        toast.success('Profile updated successfully!');
      } else {
        // Create new profile
        const response = await axios.post(`${API}/profile`, profileData);
        setUserProfile(response.data);
        // Set email field if profile has email
        if (response.data.email && !emailAddress) {
          setEmailAddress(response.data.email);
        }
        toast.success('Profile created successfully!');
      }
      setShowProfile(false);
    } catch (error) {
      console.error('Error saving profile:', error);
      toast.error('Error saving profile. Please try again.');
    }
  };

  const loadProfile = async (profileId) => {
    try {
      const response = await axios.get(`${API}/profile/${profileId}`);
      setUserProfile(response.data);
    } catch (error) {
      console.error('Error loading profile:', error);
    }
  };

  // Email grocery list function
  const emailGroceryList = async () => {
    if (!emailAddress) {
      toast.error('Please enter your email address');
      return;
    }
    
    if (!groceryList) {
      toast.error('No grocery list to email');
      return;
    }
    
    setEmailLoading(true);
    try {
      const response = await axios.post(`${API}/email-grocery-list`, {
        email: emailAddress,
        grocery_list_data: groceryList,
        user_name: userProfile?.name || null
      });
      
      if (response.data.status === 'success') {
        toast.success(`Grocery list sent to ${emailAddress}!`);
        setEmailAddress(''); // Clear email field after successful send
      }
    } catch (error) {
      console.error('Error emailing grocery list:', error);
      toast.error('Error sending email. Please try again.');
    }
    setEmailLoading(false);
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

  // Profile Component
  const ProfileForm = () => {
    const [formData, setFormData] = useState({
      name: userProfile?.name || '',
      email: userProfile?.email || '',
      household_size: userProfile?.household_size || 4,
      dietary_preferences: userProfile?.dietary_preferences || [],
      food_allergies: userProfile?.food_allergies || [],
      cuisine_preferences: userProfile?.cuisine_preferences || [],
      budget_range: userProfile?.budget_range || 'moderate',
      cooking_skill: userProfile?.cooking_skill || 'beginner',
      preferred_meal_types: userProfile?.preferred_meal_types || ['dinner']
    });

    const dietaryOptions = ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'keto', 'paleo', 'low-carb', 'low-sodium'];
    const allergyOptions = ['nuts', 'shellfish', 'eggs', 'dairy', 'soy', 'gluten', 'fish'];
    const cuisineOptions = ['italian', 'asian', 'mexican', 'indian', 'mediterranean', 'american', 'french', 'thai'];
    const mealTypeOptions = ['breakfast', 'lunch', 'dinner', 'snacks'];

    const handleCheckboxChange = (value, field) => {
      setFormData(prev => ({
        ...prev,
        [field]: prev[field].includes(value)
          ? prev[field].filter(item => item !== value)
          : [...prev[field], value]
      }));
    };

    const handleSubmit = (e) => {
      e.preventDefault();
      saveProfile(formData);
    };

    return (
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              placeholder="Your name"
            />
          </div>
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              placeholder="your@email.com"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="household_size">Household Size</Label>
          <Input
            id="household_size"
            type="number"
            min="1"
            max="10"
            value={formData.household_size}
            onChange={(e) => setFormData(prev => ({ ...prev, household_size: parseInt(e.target.value) || 4 }))}
          />
        </div>

        <div>
          <Label>Dietary Preferences</Label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
            {dietaryOptions.map(option => (
              <div key={option} className="flex items-center space-x-2">
                <Checkbox
                  id={`diet-${option}`}
                  checked={formData.dietary_preferences.includes(option)}
                  onCheckedChange={() => handleCheckboxChange(option, 'dietary_preferences')}
                />
                <Label htmlFor={`diet-${option}`} className="text-sm capitalize">
                  {option}
                </Label>
              </div>
            ))}
          </div>
        </div>

        <div>
          <Label>Food Allergies</Label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
            {allergyOptions.map(option => (
              <div key={option} className="flex items-center space-x-2">
                <Checkbox
                  id={`allergy-${option}`}
                  checked={formData.food_allergies.includes(option)}
                  onCheckedChange={() => handleCheckboxChange(option, 'food_allergies')}
                />
                <Label htmlFor={`allergy-${option}`} className="text-sm capitalize">
                  {option}
                </Label>
              </div>
            ))}
          </div>
        </div>

        <div>
          <Label>Preferred Cuisines</Label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
            {cuisineOptions.map(option => (
              <div key={option} className="flex items-center space-x-2">
                <Checkbox
                  id={`cuisine-${option}`}
                  checked={formData.cuisine_preferences.includes(option)}
                  onCheckedChange={() => handleCheckboxChange(option, 'cuisine_preferences')}
                />
                <Label htmlFor={`cuisine-${option}`} className="text-sm capitalize">
                  {option}
                </Label>
              </div>
            ))}
          </div>
        </div>

        <div>
          <Label>Preferred Meal Types</Label>
          <div className="flex gap-4 mt-2">
            {mealTypeOptions.map(option => (
              <div key={option} className="flex items-center space-x-2">
                <Checkbox
                  id={`meal-${option}`}
                  checked={formData.preferred_meal_types.includes(option)}
                  onCheckedChange={() => handleCheckboxChange(option, 'preferred_meal_types')}
                />
                <Label htmlFor={`meal-${option}`} className="text-sm capitalize">
                  {option}
                </Label>
              </div>
            ))}
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="budget_range">Budget Range</Label>
            <Select value={formData.budget_range} onValueChange={(value) => setFormData(prev => ({ ...prev, budget_range: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="Select budget range" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="budget">Budget ($20-50/week)</SelectItem>
                <SelectItem value="moderate">Moderate ($50-100/week)</SelectItem>
                <SelectItem value="premium">Premium ($100+/week)</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="cooking_skill">Cooking Skill</Label>
            <Select value={formData.cooking_skill} onValueChange={(value) => setFormData(prev => ({ ...prev, cooking_skill: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="Select cooking skill" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="beginner">Beginner</SelectItem>
                <SelectItem value="intermediate">Intermediate</SelectItem>
                <SelectItem value="advanced">Advanced</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex gap-4 pt-4">
          <Button type="submit" className="flex-1">
            {userProfile ? 'Update Profile' : 'Create Profile'}
          </Button>
          <Button type="button" variant="outline" onClick={() => setShowProfile(false)}>
            Cancel
          </Button>
        </div>
      </form>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-teal-50">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-green-50 via-blue-50 to-teal-50 shadow-sm border-b border-blue-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="flex justify-between items-center mb-8">
              <div></div>
              <div className="text-center">
                <div className="mb-6">
                  <img 
                    src={process.env.REACT_APP_LOGO_URL}
                    alt="SaleSavor Logo"
                    className="h-24 w-auto mx-auto mb-2 max-w-xs object-contain"
                    style={{
                      filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))',
                      imageRendering: 'crisp-edges'
                    }}
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <Dialog open={showProfile} onOpenChange={setShowProfile}>
                  <DialogTrigger asChild>
                    <Button variant="outline" size="sm" data-testid="profile-button" className="border-slate-300 text-slate-700 hover:bg-slate-50">
                      <User className="h-4 w-4 mr-2" />
                      {userProfile ? 'Profile' : 'Create Profile'}
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
                    <DialogHeader>
                      <DialogTitle>
                        {userProfile ? 'Update Your Profile' : 'Create Your Profile'}
                      </DialogTitle>
                    </DialogHeader>
                    <ProfileForm />
                  </DialogContent>
                </Dialog>
              </div>
            </div>
            <p className="mt-4 max-w-md mx-auto text-lg text-slate-700 sm:text-xl md:mt-6 md:text-2xl md:max-w-3xl font-medium">
              Bringing Family Meals Home - For Less
            </p>
            <div className="mt-8 relative">
              <img 
                src={process.env.REACT_APP_HERO_IMAGE_URL} 
                alt="Family Grocery Shopping" 
                className="mx-auto h-80 w-full max-w-2xl object-cover rounded-2xl shadow-2xl border-4 border-white"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-blue-900/20 via-transparent to-transparent rounded-2xl max-w-2xl mx-auto h-80"></div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Step Indicator */}
        <div className="flex justify-center mb-8">
          <div className="flex space-x-4">
            {[
              { key: 'location', label: 'Location', icon: MapPin, completed: userLocation !== null },
              { key: 'stores', label: 'Stores', icon: ShoppingCart, completed: nearbyStores.length > 0 },
              { key: 'sales', label: 'Sales', icon: DollarSign, completed: saleItems.length > 0 },
              { key: 'recipes', label: 'Recipes', icon: ChefHat, completed: generatedRecipes.length > 0 },
              { key: 'groceryList', label: 'List', icon: ShoppingCart, completed: groceryList !== null }
            ].map(({ key, label, icon: Icon, completed }) => {
              const isAccessible = completed || currentStep === key || 
                // Allow going back to previous steps
                (key === 'location') ||
                (key === 'stores' && userLocation !== null) ||
                (key === 'sales' && nearbyStores.length > 0 && selectedStore !== null) ||
                (key === 'recipes' && saleItems.length > 0);
              
              return (
                <button 
                  key={key} 
                  onClick={() => {
                    if (isAccessible) {
                      if (key === 'sales' && selectedStore && saleItems.length === 0) {
                        // Auto-load sales when navigating to sales tab
                        getStoreSales(selectedStore.id);
                      }
                      if (key === 'recipes' && saleItems.length > 0 && generatedRecipes.length === 0) {
                        // Auto-generate recipes when navigating to recipes tab
                        generateRecipes();
                      }
                      setCurrentStep(key);
                    }
                  }}
                  disabled={!isAccessible}
                  className={`flex items-center space-x-2 px-4 py-3 rounded-xl transition-all shadow-sm ${
                    currentStep === key 
                      ? 'bg-teal-100 text-teal-900 ring-2 ring-teal-400 shadow-md transform scale-105' 
                      : isAccessible 
                        ? 'bg-white text-slate-700 hover:bg-slate-50 cursor-pointer hover:shadow-md border border-slate-200 hover:border-teal-300' 
                        : 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
                  }`}>
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{label}</span>
                  {completed && currentStep !== key && (
                    <span className="text-xs text-teal-700 bg-teal-100 rounded-full px-1.5 py-0.5">✓</span>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Location Step */}
        {currentStep === 'location' && (
          <Card className="max-w-md mx-auto shadow-xl border-slate-200" data-testid="location-card">
            <CardHeader className="bg-slate-50 border-b border-slate-200">
              <CardTitle className="text-center text-slate-800">Find Stores Near You</CardTitle>
            </CardHeader>
            <CardContent className="text-center p-6">
              <p className="text-slate-700 mb-4">
                We'll find grocery stores within 25km of your location to show you the best deals
              </p>
              
              {/* Permission Notice */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4 text-left">
                <div className="flex items-start">
                  <svg className="h-4 w-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                  <div className="text-xs text-blue-800">
                    <p className="font-medium mb-1">Location Permission Required</p>
                    <p>
                      By clicking "Get My Location", you consent to sharing your location to find nearby grocery stores. 
                      Your location data is used only for store discovery and is not stored or shared.
                    </p>
                  </div>
                </div>
              </div>
              <Button 
                onClick={getCurrentLocation} 
                disabled={loading}
                className="w-full bg-teal-600 hover:bg-teal-700 text-white py-3 rounded-xl shadow-lg transform transition-all hover:scale-105"
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
            
            {/* Price Match Explanation */}
            <div className="bg-teal-50 border border-teal-200 rounded-xl p-6 mb-6 max-w-4xl mx-auto shadow-sm">
              <div className="flex items-center mb-3">
                <DollarSign className="h-5 w-5 text-teal-700 mr-2" />
                <h3 className="font-semibold text-teal-900">Price Match Policies</h3>
              </div>
              <p className="text-sm text-teal-800">
                Stores with price matching will honor competitors' advertised prices, helping you save more money. 
                Some stores even beat competitor prices by an additional percentage!
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
              {nearbyStores.slice(0, 6).map((store) => (
                <Card 
                  key={store.id} 
                  className={`cursor-pointer transition-all shadow-md hover:shadow-xl border-2 rounded-xl ${
                    selectedStore?.id === store.id ? 'ring-2 ring-emerald-500 bg-emerald-50 border-emerald-300' : 'hover:shadow-lg border-emerald-100 hover:border-emerald-200'
                  }`}
                  onClick={() => setSelectedStore(store)}
                  data-testid={`store-card-${store.chain.toLowerCase()}`}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start space-x-3">
                      <div 
                        className="h-12 w-12 rounded-lg flex items-center justify-center text-white font-bold text-lg shadow-md"
                        style={{ backgroundColor: store.brand_color || '#6B7280' }}
                      >
                        {store.logo_url ? (
                          <img 
                            src={store.logo_url}
                            alt={`${store.chain} logo`}
                            className="h-12 w-12 rounded-lg"
                            onError={(e) => {
                              // Fallback to first letter of chain if image fails
                              e.target.style.display = 'none';
                              e.target.nextElementSibling.style.display = 'flex';
                            }}
                          />
                        ) : null}
                        <span 
                          className="h-12 w-12 rounded-lg flex items-center justify-center text-white font-bold text-lg"
                          style={{ display: store.logo_url ? 'none' : 'flex' }}
                        >
                          {store.chain.charAt(0)}
                        </span>
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{store.name}</h3>
                        <p className="text-sm text-gray-600">{store.chain}</p>
                        <p className="text-xs text-gray-500 mt-1">{store.address}</p>
                        <div className="flex flex-wrap gap-2 mt-2">
                          <Badge variant="secondary">
                            {store.distance_km} km away
                          </Badge>
                          {store.price_match_policy?.has_price_match ? (
                            <Badge className="bg-emerald-100 text-emerald-800 hover:bg-emerald-100 border-emerald-300">
                              <DollarSign className="h-3 w-3 mr-1" />
                              Price Match
                              {store.price_match_policy.additional_discount > 0 && 
                                ` +${store.price_match_policy.additional_discount}%`
                              }
                            </Badge>
                          ) : (
                            <Badge variant="outline" className="text-gray-500 border-gray-300">
                              No Price Match
                            </Badge>
                          )}
                        </div>
                        {store.price_match_policy?.has_price_match && (
                          <div className="mt-2">
                            <p className="text-xs text-emerald-700 font-medium">
                              {store.price_match_policy.policy_name}
                            </p>
                            <p className="text-xs text-emerald-600 mt-1">
                              {store.price_match_policy.description}
                            </p>
                          </div>
                        )}
                        {store.flyer_url && (
                          <div className="mt-3">
                            <a
                              href={store.flyer_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center text-xs text-teal-600 hover:text-teal-800 font-medium transition-colors"
                            >
                              <ExternalLink className="h-3 w-3 mr-1" />
                              View Current Flyer
                            </a>
                          </div>
                        )}
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
                  className="bg-teal-600 hover:bg-teal-700 text-white px-8 py-3 rounded-xl shadow-lg transform transition-all hover:scale-105"
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
            
            {/* Price Verification Notice */}
            <div className="bg-orange-50 border border-orange-200 rounded-xl p-4 mb-6 max-w-4xl mx-auto">
              <div className="flex items-center mb-2">
                <svg className="h-5 w-5 text-orange-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <h3 className="font-semibold text-orange-900">Please Verify Prices In-Store</h3>
              </div>
              <p className="text-sm text-orange-800">
                These prices are estimates based on available sales data. <strong>Always confirm pricing, availability, and promotional terms at the store</strong> before shopping. 
                Sales may have ended, items may be out of stock, or additional conditions may apply.
              </p>
            </div>
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
            <div className="text-center mt-8">
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-6 mb-6 max-w-2xl mx-auto">
                <div className="flex items-center justify-center mb-3">
                  <ChefHat className="h-6 w-6 text-emerald-600 mr-2" />
                  <h3 className="font-bold text-emerald-800 text-lg">Ready for AI Meal Planning?</h3>
                </div>
                <p className="text-emerald-700 mb-4">
                  Based on these amazing sale prices, we'll create personalized family-friendly recipes 
                  that help you save money and bring delicious meals home!
                </p>
                <Button 
                  onClick={generateRecipes} 
                  disabled={loading}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-4 rounded-xl shadow-lg transform transition-all hover:scale-105 text-lg font-semibold"
                  data-testid="generate-recipes-btn"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Generating Recipes...
                    </>
                  ) : (
                    <>
                      <ChefHat className="h-5 w-5 mr-2" />
                      Generate Meal Ideas
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Recipes Step - With Recipes */}
        {currentStep === 'recipes' && generatedRecipes.length > 0 && (
          <div data-testid="recipes-section">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold text-emerald-800">
                Choose Your Favorite Recipes
              </h2>
              <p className="text-lg text-emerald-700 mt-2 mb-1">
                Select the meals you'd like to cook this week
              </p>
              {userProfile && (
                <p className="text-sm text-emerald-600 mt-2">
                  ✨ Personalized for {userProfile.name || 'you'} • 
                  {userProfile.dietary_preferences.length > 0 && (
                    <span> {userProfile.dietary_preferences.join(', ')} • </span>
                  )}
                  {userProfile.household_size} people
                </p>
              )}
              <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3 mt-4 max-w-2xl mx-auto">
                <p className="text-sm text-emerald-700">
                  💡 <strong>Tip:</strong> Click on any recipe card to select it, then we'll create your optimized grocery list with the best prices!
                </p>
              </div>
            </div>
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
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <div className="flex items-center justify-center mb-2">
                  <ChefHat className="h-5 w-5 text-blue-600 mr-2" />
                  <h3 className="font-medium text-blue-800">Choose Your Recipes</h3>
                </div>
                <p className="text-sm text-blue-700">
                  Click on the recipe cards above to select the meals you'd like to cook. 
                  We'll generate an optimized shopping list for your selections.
                </p>
              </div>
              
              {selectedRecipes.length > 0 ? (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <p className="text-green-800 font-medium">
                    ✓ {selectedRecipes.length} recipe{selectedRecipes.length !== 1 ? 's' : ''} selected
                  </p>
                  <p className="text-sm text-green-700">
                    Ready to create your personalized grocery list!
                  </p>
                </div>
              ) : (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                  <p className="text-yellow-800 font-medium">
                    👆 Please select at least one recipe above
                  </p>
                  <p className="text-sm text-yellow-700">
                    Click on any recipe card to select it for your meal plan
                  </p>
                </div>
              )}
              
              <Button 
                onClick={generateGroceryList} 
                disabled={loading || selectedRecipes.length === 0}
                className={selectedRecipes.length > 0 ? 'bg-green-600 hover:bg-green-700' : ''}
                data-testid="generate-grocery-list-btn"
              >
                {loading ? 'Creating Your List...' : selectedRecipes.length > 0 ? `Create List for ${selectedRecipes.length} Recipe${selectedRecipes.length !== 1 ? 's' : ''}` : 'Select Recipes First'}
              </Button>
            </div>
          </div>
        )}

        {/* Recipes Step - No Recipes Yet */}
        {currentStep === 'recipes' && generatedRecipes.length === 0 && (
          <div data-testid="recipes-placeholder" className="text-center">
            <div className="max-w-2xl mx-auto">
              <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-8 border border-emerald-200 shadow-sm">
                <div className="mb-6">
                  <div className="mx-auto w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mb-4">
                    <ChefHat className="h-10 w-10 text-emerald-600" />
                  </div>
                  <h2 className="text-2xl font-bold text-emerald-800 mb-3">
                    Ready to Create Amazing Meals?
                  </h2>
                  <p className="text-emerald-700 text-lg">
                    Let's generate personalized recipes using the best sale prices from your local stores!
                  </p>
                </div>
                
                {saleItems.length === 0 ? (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-6">
                    <p className="text-yellow-800 font-medium mb-2">📋 First, let's get your sale items</p>
                    <p className="text-sm text-yellow-700">
                      Go back to <span className="font-medium">Sales</span> to see current deals, then return here for recipe magic!
                    </p>
                    <Button 
                      onClick={() => setCurrentStep('sales')}
                      className="mt-3 bg-yellow-600 hover:bg-yellow-700 text-white"
                    >
                      View Sales First
                    </Button>
                  </div>
                ) : (
                  <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 mb-6">
                    <p className="text-emerald-800 font-medium mb-2">
                      🛒 Great! You have {saleItems.length} sale items ready
                    </p>
                    <p className="text-sm text-emerald-700 mb-4">
                      Now let's turn those deals into delicious family meals
                    </p>
                    <Button 
                      onClick={generateRecipes}
                      disabled={loading}
                      className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-3 rounded-xl shadow-lg transform transition-all hover:scale-105"
                    >
                      {loading ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                          Generating Recipes...
                        </>
                      ) : (
                        <>
                          <ChefHat className="h-5 w-5 mr-2" />
                          Generate My Recipes
                        </>
                      )}
                    </Button>
                  </div>
                )}
                
                <div className="text-center">
                  <p className="text-sm text-emerald-600 mb-4">
                    ✨ Our AI will create recipes based on your sale items 
                    {userProfile && userProfile.dietary_preferences.length > 0 && 
                      ` and your ${userProfile.dietary_preferences.join(', ')} preferences`
                    }
                  </p>
                </div>
              </div>
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
                    <p className="text-sm text-gray-600">Estimated Total</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-red-600">${groceryList.total_savings.toFixed(2)}</p>
                    <p className="text-sm text-gray-600">Estimated Savings</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-blue-600">{groceryList.items.length}</p>
                    <p className="text-sm text-gray-600">Items</p>
                  </div>
                </div>
                
                {/* Estimate Disclaimer */}
                <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-xs text-yellow-800 text-center">
                    💡 <strong>Estimates Only:</strong> Prices and savings are estimates. Always verify current prices, 
                    availability, and store policies before shopping. Actual totals may vary.
                  </p>
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
              {/* Email Grocery List Section */}
              <Card className="mb-6 max-w-md mx-auto">
                <CardHeader className="bg-teal-50 border-b border-teal-200">
                  <CardTitle className="text-center text-teal-900 flex items-center justify-center">
                    📧 Email Your Grocery List
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  <p className="text-slate-700 text-sm mb-4">
                    Get this list delivered to your inbox! Perfect for easy mobile shopping.
                  </p>
                  <div className="space-y-4">
                    <Input
                      type="email"
                      placeholder="Enter your email address"
                      value={emailAddress}
                      onChange={(e) => setEmailAddress(e.target.value)}
                      className="w-full"
                    />
                    <Button 
                      onClick={emailGroceryList}
                      disabled={emailLoading || !emailAddress}
                      className="w-full bg-teal-600 hover:bg-teal-700 text-white py-2.5 rounded-xl shadow-lg transform transition-all hover:scale-105"
                    >
                      {emailLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Sending Email...
                        </>
                      ) : (
                        <>
                          📧 Send Grocery List
                        </>
                      )}
                    </Button>
                  </div>
                  <div className="mt-4 p-3 bg-slate-50 rounded-lg">
                    <p className="text-xs text-slate-600">
                      💡 <strong>Why email?</strong> Have your list on your phone while shopping, 
                      share with family members, or keep for your records!
                    </p>
                  </div>
                </CardContent>
              </Card>
              
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
      
      {/* Legal Disclaimers Footer */}
      <footer className="bg-slate-100 border-t border-slate-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Price Verification Warning */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-semibold text-yellow-800">
                  ⚠️ Important: Always Verify Prices Before Shopping
                </h3>
                <p className="text-sm text-yellow-700 mt-1">
                  Prices and promotions shown are estimates based on available data and may not reflect current in-store prices. 
                  Always verify prices, availability, and promotional terms directly with the store before making purchases. 
                  Store policies and prices change frequently.
                </p>
              </div>
            </div>
          </div>

          {/* Legal Disclaimers */}
          <div className="grid md:grid-cols-2 gap-6 text-sm text-slate-600">
            <div>
              <h4 className="font-semibold text-slate-800 mb-2">Service Disclaimer</h4>
              <p className="mb-3">
                SaleSavor is a grocery planning assistant that aggregates publicly available sales information and generates meal suggestions. 
                We do not guarantee price accuracy, product availability, or store policy compliance.
              </p>
              <p className="mb-3">
                <strong>Use of this service is at your own risk.</strong> We are not responsible for any financial loss, 
                inconvenience, or issues arising from reliance on the information provided.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold text-slate-800 mb-2">Data & Privacy</h4>
              <p className="mb-3">
                By using SaleSavor, you consent to the collection and use of location data to find nearby stores and 
                dietary preferences to personalize recommendations. We do not store payment information or share personal data with third parties.
              </p>
              <p className="mb-3">
                Recipe suggestions are generated using AI and may not be suitable for all dietary restrictions or allergies. 
                Always review ingredients carefully, especially if you have food allergies or medical dietary requirements.
              </p>
            </div>
          </div>

          {/* Terms & Contact */}
          <div className="border-t border-slate-200 mt-6 pt-6 text-center">
            <p className="text-xs text-slate-500">
              © {new Date().getFullYear()} SaleSavor. This service is provided "as-is" without warranties of any kind. 
              By using this application, you agree to verify all pricing information independently and acknowledge that 
              store policies, prices, and availability may differ from what is displayed.
            </p>
            <p className="text-xs text-slate-500 mt-2">
              For questions or concerns, please contact your local grocery stores directly for the most accurate pricing and policy information.
            </p>
          </div>
        </div>
      </footer>
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
