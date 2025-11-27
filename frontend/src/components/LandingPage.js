import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { MapPin, ChefHat, ShoppingCart, Apple, Play, ArrowRight } from 'lucide-react';
import AdSenseAd from './AdSenseAd';

const LandingPage = ({ onGetStarted }) => {
  const appStoreUrl = process.env.REACT_APP_APP_STORE_URL || '#';
  const googlePlayUrl = process.env.REACT_APP_GOOGLE_PLAY_URL || '#';

  const scrollToSales = () => {
    if (onGetStarted) {
      onGetStarted();
    } else {
      window.location.href = '/sales';
    }
  };

  return (
    <div className="min-h-screen" style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      {/* Hero Section */}
      <section className="min-h-screen flex items-center px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#f5f5f5' }}>
        <div className="max-w-7xl mx-auto w-full">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Hero Content */}
            <div className="text-center lg:text-left">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6" style={{ color: '#1a1a1a', lineHeight: '1.2' }}>
                Save Money, Eat Better!
              </h1>
              <p className="text-xl md:text-2xl mb-8 leading-relaxed" style={{ color: '#666666' }}>
                Smart Grocery Shopping Made Easy - Find the best deals and get personalized recipe suggestions
              </p>
              
              {/* App Store Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start mb-6">
                <Button 
                  className="flex items-center gap-3 px-8 py-6 text-lg font-bold rounded-xl shadow-lg transform hover:scale-105 transition-all"
                  style={{ backgroundColor: '#2c5f2d', color: '#ffffff' }}
                  onClick={() => window.open(appStoreUrl, '_blank')}
                >
                  <Apple className="h-6 w-6" />
                  Download on App Store
                </Button>
                <Button 
                  className="flex items-center gap-3 px-8 py-6 text-lg font-bold rounded-xl shadow-lg transform hover:scale-105 transition-all"
                  style={{ backgroundColor: '#2c5f2d', color: '#ffffff' }}
                  onClick={() => window.open(googlePlayUrl, '_blank')}
                >
                  <Play className="h-6 w-6" />
                  Get it on Google Play
                </Button>
              </div>
              
              {/* Browse Sales Link */}
              <div className="flex flex-col sm:flex-row gap-4 items-center">
                <button 
                  onClick={scrollToSales}
                  className="inline-flex items-center gap-2 text-lg font-medium hover:underline transition-colors"
                  style={{ color: '#3030F1' }}
                >
                  Try the web app <ArrowRight className="h-5 w-5" />
                </button>
                <span style={{ color: '#666666' }}>|</span>
                <button 
                  onClick={scrollToSales}
                  className="inline-flex items-center gap-2 text-lg font-medium hover:underline transition-colors"
                  style={{ color: '#3030F1' }}
                >
                  Browse this week's sales <ArrowRight className="h-5 w-5" />
                </button>
              </div>
            </div>
            
            {/* Hero Image - App Screenshots */}
            <div className="flex justify-center lg:justify-end">
              <div className="relative">
                {/* Main hero screenshot */}
                <img 
                  src={process.env.REACT_APP_HERO_SCREENSHOT} 
                  alt="SaleSavor Mobile App Welcome Screen" 
                  className="w-72 h-auto rounded-3xl shadow-2xl border-4 border-white"
                  style={{ borderRadius: '24px' }}
                />
                
                {/* Floating secondary screenshots */}
                <img 
                  src={process.env.REACT_APP_STORES_SCREENSHOT}
                  alt="Shopping List Screen" 
                  className="absolute -right-8 top-16 w-48 h-auto rounded-2xl shadow-xl border-2 border-white opacity-90"
                  style={{ borderRadius: '16px', transform: 'rotate(8deg)' }}
                />
                
                <img 
                  src="https://customer-assets.emergentagent.com/job_grocery-saver-4/artifacts/h0swgs35_app6.JPG"
                  alt="Recipe Details" 
                  className="absolute -left-6 bottom-8 w-44 h-auto rounded-2xl shadow-xl border-2 border-white opacity-85"
                  style={{ borderRadius: '16px', transform: 'rotate(-5deg)' }}
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Features Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#ffffff' }}>
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
              Smart Grocery Shopping Made Simple
            </h2>
            <p className="text-xl" style={{ color: '#666666' }}>
              Everything you need to save money and eat well
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <Card className="text-center p-8 h-full shadow-lg hover:shadow-xl transition-shadow" style={{ borderRadius: '12px' }}>
              <CardContent className="p-0">
                <div className="text-6xl mb-6">📍</div>
                <h3 className="text-2xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
                  Discover Local Sales
                </h3>
                <p className="text-lg leading-relaxed" style={{ color: '#666666' }}>
                  Automatically find weekly sales from Loblaws, Sobeys, Metro, and Walmart near you
                </p>
              </CardContent>
            </Card>
            
            {/* Feature 2 */}
            <Card className="text-center p-8 h-full shadow-lg hover:shadow-xl transition-shadow" style={{ borderRadius: '12px' }}>
              <CardContent className="p-0">
                <div className="text-6xl mb-6">🤖</div>
                <h3 className="text-2xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
                  Personalized Recipes
                </h3>
                <p className="text-lg leading-relaxed" style={{ color: '#666666' }}>
                  Get recipe recommendations tailored to your dietary needs and available sales
                </p>
              </CardContent>
            </Card>
            
            {/* Feature 3 */}
            <Card className="text-center p-8 h-full shadow-lg hover:shadow-xl transition-shadow" style={{ borderRadius: '12px' }}>
              <CardContent className="p-0">
                <div className="text-6xl mb-6">📝</div>
                <h3 className="text-2xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
                  Save Time & Money
                </h3>
                <p className="text-lg leading-relaxed" style={{ color: '#666666' }}>
                  Generate optimized shopping lists and email them to yourself
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#f5f5f5' }}>
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
              How It Works
            </h2>
            <p className="text-xl" style={{ color: '#666666' }}>
              Three simple steps to start saving
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-12">
            {/* Step 1 */}
            <div className="text-center">
              <img 
                src={process.env.REACT_APP_PROFILE_SCREENSHOT}
                alt="Set Your Preferences" 
                className="w-48 h-auto mx-auto mb-6 rounded-xl shadow-lg"
                style={{ borderRadius: '16px' }}
              />
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-lg font-bold text-white mx-auto mb-4" 
                   style={{ backgroundColor: '#2c5f2d' }}>
                1
              </div>
              <h3 className="text-2xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
                Set Your Preferences
              </h3>
              <p className="text-lg leading-relaxed" style={{ color: '#666666' }}>
                Tell us your family size, dietary needs, and health concerns
              </p>
            </div>
            
            {/* Step 2 */}
            <div className="text-center">
              <img 
                src="https://customer-assets.emergentagent.com/job_grocery-saver-4/artifacts/tmd2be6u_app7.JPG"
                alt="See What's On Sale" 
                className="w-48 h-auto mx-auto mb-6 rounded-xl shadow-lg"
                style={{ borderRadius: '16px' }}
              />
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-lg font-bold text-white mx-auto mb-4" 
                   style={{ backgroundColor: '#2c5f2d' }}>
                2
              </div>
              <h3 className="text-2xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
                See What's On Sale
              </h3>
              <p className="text-lg leading-relaxed" style={{ color: '#666666' }}>
                Browse weekly flyers from nearby grocery stores
              </p>
            </div>
            
            {/* Step 3 */}
            <div className="text-center">
              <img 
                src="https://customer-assets.emergentagent.com/job_grocery-saver-4/artifacts/70a24v7g_app8.JPG"
                alt="Get Recipe Ideas" 
                className="w-48 h-auto mx-auto mb-6 rounded-xl shadow-lg"
                style={{ borderRadius: '16px' }}
              />
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-lg font-bold text-white mx-auto mb-4" 
                   style={{ backgroundColor: '#2c5f2d' }}>
                3
              </div>
              <h3 className="text-2xl font-bold mb-4" style={{ color: '#1a1a1a' }}>
                Get Recipe Ideas
              </h3>
              <p className="text-lg leading-relaxed" style={{ color: '#666666' }}>
                Receive AI-powered recipe suggestions based on sales and your profile
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Download CTA Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#2c5f2d' }}>
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4" style={{ color: '#ffffff' }}>
            Ready to Start Saving?
          </h2>
          <p className="text-xl mb-8" style={{ color: '#ffffff', opacity: 0.9 }}>
            Join thousands of Canadian families cutting their grocery bills
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-6">
            <Button 
              className="flex items-center gap-3 px-8 py-6 text-lg font-bold rounded-xl shadow-lg transform hover:scale-105 transition-all"
              style={{ backgroundColor: '#ffffff', color: '#2c5f2d' }}
              onClick={() => window.open(appStoreUrl, '_blank')}
            >
              <Apple className="h-6 w-6" />
              Download on App Store
            </Button>
            <Button 
              className="flex items-center gap-3 px-8 py-6 text-lg font-bold rounded-xl shadow-lg transform hover:scale-105 transition-all"
              style={{ backgroundColor: '#ffffff', color: '#2c5f2d' }}
              onClick={() => window.open(googlePlayUrl, '_blank')}
            >
              <Play className="h-6 w-6" />
              Get it on Google Play
            </Button>
          </div>
          
          <p className="text-sm" style={{ color: '#ffffff', opacity: 0.8 }}>
            Available on iOS and Android
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#1a1a1a' }}>
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            {/* Left Column */}
            <div>
              <img 
                src={process.env.REACT_APP_LOGO_URL} 
                alt="SaleSavor Logo" 
                className="h-8 mb-4"
              />
              <p style={{ color: '#ffffff', opacity: 0.8 }}>
                © 2025 SaleSavor. All rights reserved.
              </p>
            </div>
            
            {/* Center Column */}
            <div>
              <div className="space-y-2">
                <a href="/privacy-policy" className="block hover:underline" style={{ color: '#ffffff', opacity: 0.8 }}>
                  Privacy Policy
                </a>
                <a href="/terms-of-service" className="block hover:underline" style={{ color: '#ffffff', opacity: 0.8 }}>
                  Terms of Service
                </a>
                <a href="#" className="termly-display-preferences block hover:underline" style={{ color: '#ffffff', opacity: 0.8 }}>
                  Cookie Preferences
                </a>
              </div>
            </div>
            
            {/* Right Column */}
            <div>
              <div className="space-y-2" style={{ color: '#ffffff', opacity: 0.8 }}>
                <p>Contact: info@salesavor.ca</p>
                <p>Phone: 1-613-246-5411</p>
                <p>Kingston, Ontario, Canada</p>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;