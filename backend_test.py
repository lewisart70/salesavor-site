import requests
import sys
import json
from datetime import datetime

class GrocerySavingsAPITester:
    def __init__(self, base_url="https://meal-saver-4.preview.emergentagent.com"):
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