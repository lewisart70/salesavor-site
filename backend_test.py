import requests
import sys
import json
from datetime import datetime

class GrocerySavingsAPITester:
    def __init__(self, base_url="https://grocery-saver-4.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")

            self.test_results.append({
                'name': name,
                'success': success,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'response_size': len(response.text) if response.text else 0
            })

            return success, response.json() if success and response.text else {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            self.test_results.append({
                'name': name,
                'success': False,
                'error': 'Timeout',
                'timeout': timeout
            })
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                'name': name,
                'success': False,
                'error': str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_nearby_stores(self):
        """Test finding nearby stores"""
        # Toronto coordinates for testing
        location_data = {
            "latitude": 43.6532,
            "longitude": -79.3832,
            "address": "Toronto, ON"
        }
        
        success, response = self.run_test(
            "Find Nearby Stores",
            "POST",
            "stores/nearby",
            200,
            data=location_data
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   Found {len(response)} stores")
            first_store = response[0]
            print(f"   First store: {first_store.get('name', 'Unknown')} - {first_store.get('distance_km', 'Unknown')} km")
            return success, response
        elif success:
            print("   Warning: No stores found in response")
            
        return success, response

    def test_store_sales(self, store_id="test-store-123"):
        """Test getting store sales"""
        success, response = self.run_test(
            "Get Store Sales",
            "GET",
            f"stores/{store_id}/sales",
            200
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   Found {len(response)} sale items")
            first_item = response[0]
            print(f"   First item: {first_item.get('name', 'Unknown')} - ${first_item.get('sale_price', 0):.2f}")
            return success, response
        elif success:
            print("   Warning: No sale items found in response")
            
        return success, response

    def test_recipe_generation(self, sale_items=None):
        """Test AI recipe generation"""
        if not sale_items:
            # Use mock sale items for testing
            sale_items = [
                {"name": "Ground Beef (1 lb)", "original_price": 6.99, "sale_price": 4.99, "discount_percentage": 29, "category": "Meat"},
                {"name": "Pasta (500g)", "original_price": 2.49, "sale_price": 1.49, "discount_percentage": 40, "category": "Pantry"},
                {"name": "Tomatoes (1 lb)", "original_price": 3.99, "sale_price": 2.49, "discount_percentage": 38, "category": "Produce"}
            ]
        
        recipe_request = {
            "sale_items": sale_items,
            "dietary_preferences": [],
            "servings": 4
        }
        
        # Increase timeout for AI generation
        success, response = self.run_test(
            "Generate AI Recipes",
            "POST",
            "recipes/generate",
            200,
            data=recipe_request,
            timeout=60  # Longer timeout for AI processing
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   Generated {len(response)} recipes")
            first_recipe = response[0]
            print(f"   First recipe: {first_recipe.get('name', 'Unknown')} - ${first_recipe.get('estimated_cost', 0):.2f}")
            return success, response
        elif success:
            print("   Warning: No recipes generated")
            
        return success, response

    def test_grocery_list_generation(self, recipes=None):
        """Test grocery list generation"""
        if not recipes:
            recipes = ["recipe-1", "recipe-2"]  # Mock recipe IDs
        
        grocery_request = {
            "user_location": {
                "latitude": 43.6532,
                "longitude": -79.3832,
                "address": "Toronto, ON"
            },
            "selected_recipes": recipes,
            "servings_multiplier": 1.0
        }
        
        success, response = self.run_test(
            "Generate Grocery List",
            "POST",
            "grocery-list/generate",
            200,
            data=grocery_request
        )
        
        if success and isinstance(response, dict):
            items = response.get('items', [])
            total_cost = response.get('total_cost', 0)
            total_savings = response.get('total_savings', 0)
            print(f"   Generated list with {len(items)} items")
            print(f"   Total cost: ${total_cost:.2f}, Savings: ${total_savings:.2f}")
            return success, response
        elif success:
            print("   Warning: Invalid grocery list response format")
            
        return success, response

    def test_user_profile_crud(self):
        """Test user profile CRUD operations"""
        # Test data with dietary preferences as specified in review request
        profile_data = {
            "name": "Sarah Johnson",
            "email": "sarah.test@example.com",
            "household_size": 4,
            "dietary_preferences": ["vegetarian", "gluten-free"],
            "food_allergies": ["nuts"],
            "cuisine_preferences": ["italian", "mediterranean"],
            "budget_range": "moderate",
            "cooking_skill": "intermediate",
            "preferred_meal_types": ["dinner", "lunch"]
        }
        
        # Test 1: Create Profile
        create_success, create_response = self.run_test(
            "Create User Profile",
            "POST",
            "profile",
            200,
            data=profile_data
        )
        
        if not create_success:
            return False, {}
        
        profile_id = create_response.get('id')
        if not profile_id:
            print("   Error: No profile ID returned from create")
            return False, {}
        
        print(f"   Created profile with ID: {profile_id}")
        
        # Test 2: Get Profile
        get_success, get_response = self.run_test(
            "Get User Profile",
            "GET",
            f"profile/{profile_id}",
            200
        )
        
        if get_success:
            print(f"   Retrieved profile: {get_response.get('name', 'Unknown')}")
        
        # Test 3: Update Profile
        update_data = {
            "household_size": 5,
            "dietary_preferences": ["vegetarian", "gluten-free", "dairy-free"],
            "budget_range": "premium"
        }
        
        update_success, update_response = self.run_test(
            "Update User Profile",
            "PUT",
            f"profile/{profile_id}",
            200,
            data=update_data
        )
        
        if update_success:
            print(f"   Updated profile household size: {update_response.get('household_size', 'Unknown')}")
        
        return create_success and get_success and update_success, {
            'profile_id': profile_id,
            'profile_data': create_response
        }

    def test_email_service(self, grocery_list_data=None):
        """Test SendGrid email integration"""
        if not grocery_list_data:
            # Create mock grocery list data
            grocery_list_data = {
                "items": [
                    {
                        "ingredient": "Ground Beef (1 lb)",
                        "quantity": "1.0 lb",
                        "store_name": "Loblaws Superstore",
                        "store_id": "store-123",
                        "price": 6.99,
                        "is_on_sale": True,
                        "sale_price": 4.99
                    },
                    {
                        "ingredient": "Pasta (500g)",
                        "quantity": "1.0 package",
                        "store_name": "Metro Plus",
                        "store_id": "store-456",
                        "price": 2.49,
                        "is_on_sale": True,
                        "sale_price": 1.49
                    }
                ],
                "total_cost": 6.48,
                "total_savings": 3.00
            }
        
        email_request = {
            "email": "test.user@example.com",
            "grocery_list_data": grocery_list_data,
            "user_name": "Test User"
        }
        
        success, response = self.run_test(
            "Email Grocery List",
            "POST",
            "email-grocery-list",
            200,
            data=email_request
        )
        
        if success:
            status = response.get('status', 'unknown')
            message = response.get('message', 'No message')
            print(f"   Email status: {status}")
            print(f"   Message: {message}")
        
        return success, response

    def test_recipe_generation_with_dietary_preferences(self):
        """Test recipe generation with specific dietary preferences from review request"""
        sale_items = [
            {"name": "Bell Peppers (each)", "original_price": 2.99, "sale_price": 1.99, "discount_percentage": 33, "category": "Produce"},
            {"name": "Carrots (2 lb bag)", "original_price": 2.99, "sale_price": 1.99, "discount_percentage": 33, "category": "Produce"},
            {"name": "Rice (2 kg)", "original_price": 5.99, "sale_price": 3.99, "discount_percentage": 33, "category": "Pantry"},
            {"name": "Pasta (500g)", "original_price": 2.49, "sale_price": 1.49, "discount_percentage": 40, "category": "Pantry"}
        ]
        
        recipe_request = {
            "sale_items": sale_items,
            "dietary_preferences": ["vegetarian", "gluten-free"],  # As specified in review request
            "servings": 4
        }
        
        success, response = self.run_test(
            "Generate Recipes with Dietary Preferences",
            "POST",
            "recipes/generate",
            200,
            data=recipe_request,
            timeout=60
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   Generated {len(response)} vegetarian/gluten-free recipes")
            for i, recipe in enumerate(response[:2]):  # Show first 2 recipes
                name = recipe.get('name', 'Unknown')
                tags = recipe.get('dietary_tags', [])
                cost = recipe.get('estimated_cost', 0)
                print(f"   Recipe {i+1}: {name} (${cost:.2f}) - Tags: {tags}")
            return success, response
        elif success:
            print("   Warning: No recipes generated with dietary preferences")
            
        return success, response

def main():
    print("🛒 Starting Grocery Savings App API Tests")
    print("=" * 50)
    
    tester = GrocerySavingsAPITester()
    
    # Test 1: Root endpoint
    tester.test_root_endpoint()
    
    # Test 2: Find nearby stores
    stores_success, stores_data = tester.test_nearby_stores()
    
    # Test 3: Get store sales (use first store if available)
    store_id = "test-store-123"  # Default test ID
    if stores_success and stores_data and len(stores_data) > 0:
        store_id = stores_data[0].get('id', store_id)
    
    sales_success, sales_data = tester.test_store_sales(store_id)
    
    # Test 4: Generate recipes (use actual sale items if available)
    recipe_items = sales_data if sales_success and sales_data else None
    recipes_success, recipes_data = tester.test_recipe_generation(recipe_items)
    
    # Test 5: Generate grocery list (use actual recipe IDs if available)
    recipe_ids = None
    if recipes_success and recipes_data:
        recipe_ids = [recipe.get('id') for recipe in recipes_data if recipe.get('id')]
    
    tester.test_grocery_list_generation(recipe_ids)
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the details above.")
        
        # Print failed tests summary
        failed_tests = [test for test in tester.test_results if not test['success']]
        if failed_tests:
            print("\nFailed Tests:")
            for test in failed_tests:
                error_msg = test.get('error', f'Status {test.get("status_code", "unknown")}')
                print(f"  - {test['name']}: {error_msg}")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())