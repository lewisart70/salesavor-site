#!/usr/bin/env python3
"""
Focused test for user-reported issue: Stores not populating after clicking "Get Location"
User can create profile ✅, get location ✅, but stores don't populate ❌

This test specifically validates the location → stores flow that the user is experiencing issues with.
"""

import requests
import json
import time
from datetime import datetime

class LocationStoresFlowTester:
    def __init__(self, base_url="https://grocery-savings-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.test_results = []
        
    def log_test(self, name, success, details=""):
        """Log test result"""
        result = {
            'name': name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    {details}")
        return success

    def test_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response time: {response.elapsed.total_seconds():.2f}s"
            return self.log_test("API Connectivity", success, details)
        except Exception as e:
            return self.log_test("API Connectivity", False, f"Error: {str(e)}")

    def test_stores_nearby_basic(self):
        """Test basic /api/stores/nearby endpoint with Toronto coordinates"""
        location_data = {
            "latitude": 43.6532,
            "longitude": -79.3832,
            "address": "Toronto, ON"
        }
        
        try:
            print(f"\n🔍 Testing stores/nearby with Toronto coordinates...")
            print(f"    Request: {json.dumps(location_data, indent=2)}")
            
            response = requests.post(
                f"{self.api_url}/stores/nearby",
                json=location_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            success = response.status_code == 200
            response_time = response.elapsed.total_seconds()
            
            if success:
                stores = response.json()
                if isinstance(stores, list) and len(stores) > 0:
                    details = f"Found {len(stores)} stores in {response_time:.2f}s"
                    print(f"    Response time: {response_time:.2f}s")
                    print(f"    Stores found: {len(stores)}")
                    
                    # Log first few stores
                    for i, store in enumerate(stores[:3]):
                        name = store.get('name', 'Unknown')
                        distance = store.get('distance_km', 'Unknown')
                        print(f"    Store {i+1}: {name} ({distance} km)")
                    
                    return self.log_test("Stores Nearby - Basic", True, details)
                else:
                    return self.log_test("Stores Nearby - Basic", False, f"Empty response in {response_time:.2f}s")
            else:
                return self.log_test("Stores Nearby - Basic", False, f"Status {response.status_code}: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            return self.log_test("Stores Nearby - Basic", False, "Request timed out after 15s")
        except Exception as e:
            return self.log_test("Stores Nearby - Basic", False, f"Error: {str(e)}")

    def test_stores_nearby_timing(self):
        """Test multiple requests to check for timing/consistency issues"""
        location_data = {
            "latitude": 43.6532,
            "longitude": -79.3832,
            "address": "Toronto, ON"
        }
        
        print(f"\n⏱️  Testing timing consistency (5 requests)...")
        
        response_times = []
        store_counts = []
        failures = 0
        
        for i in range(5):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.api_url}/stores/nearby",
                    json=location_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=20
                )
                end_time = time.time()
                response_time = end_time - start_time
                
                if response.status_code == 200:
                    stores = response.json()
                    store_count = len(stores) if isinstance(stores, list) else 0
                    response_times.append(response_time)
                    store_counts.append(store_count)
                    print(f"    Request {i+1}: {response_time:.2f}s, {store_count} stores")
                else:
                    failures += 1
                    print(f"    Request {i+1}: FAILED - Status {response.status_code}")
                    
            except Exception as e:
                failures += 1
                print(f"    Request {i+1}: ERROR - {str(e)}")
        
        if failures == 0 and response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            consistent_count = len(set(store_counts)) == 1
            
            details = f"Avg: {avg_time:.2f}s, Max: {max_time:.2f}s, Consistent count: {consistent_count}"
            success = max_time < 10.0 and consistent_count  # Should be fast and consistent
            
            return self.log_test("Stores Nearby - Timing", success, details)
        else:
            return self.log_test("Stores Nearby - Timing", False, f"{failures}/5 requests failed")

    def test_stores_nearby_edge_cases(self):
        """Test edge cases that might cause frontend issues"""
        test_cases = [
            {
                "name": "Missing address field",
                "data": {"latitude": 43.6532, "longitude": -79.3832},
                "should_succeed": True
            },
            {
                "name": "Different radius",
                "data": {"latitude": 43.6532, "longitude": -79.3832, "address": "Toronto, ON"},
                "params": {"radius_km": 10},
                "should_succeed": True
            },
            {
                "name": "Far location (should return fewer stores)",
                "data": {"latitude": 45.4215, "longitude": -75.6972, "address": "Ottawa, ON"},
                "should_succeed": True
            }
        ]
        
        print(f"\n🧪 Testing edge cases...")
        
        all_passed = True
        for test_case in test_cases:
            try:
                url = f"{self.api_url}/stores/nearby"
                if test_case.get('params'):
                    params = '&'.join([f"{k}={v}" for k, v in test_case['params'].items()])
                    url += f"?{params}"
                
                response = requests.post(
                    url,
                    json=test_case['data'],
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                success = response.status_code == 200
                if success and test_case['should_succeed']:
                    stores = response.json()
                    store_count = len(stores) if isinstance(stores, list) else 0
                    details = f"{store_count} stores returned"
                    test_passed = self.log_test(f"Edge Case - {test_case['name']}", True, details)
                elif not success and not test_case['should_succeed']:
                    test_passed = self.log_test(f"Edge Case - {test_case['name']}", True, f"Expected failure: {response.status_code}")
                else:
                    test_passed = self.log_test(f"Edge Case - {test_case['name']}", False, f"Status: {response.status_code}")
                
                all_passed = all_passed and test_passed
                
            except Exception as e:
                self.log_test(f"Edge Case - {test_case['name']}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_expected_store_data_structure(self):
        """Verify the API returns the expected 8 stores with correct data structure"""
        location_data = {
            "latitude": 43.6532,
            "longitude": -79.3832,
            "address": "Toronto, ON"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/stores/nearby",
                json=location_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code != 200:
                return self.log_test("Store Data Structure", False, f"API returned {response.status_code}")
            
            stores = response.json()
            
            # Check if we get the expected 8 stores
            expected_stores = ["Loblaws", "Metro", "Food Basics", "Walmart", "Sobeys", "Costco", "FreshMart", "ValueMart"]
            
            if not isinstance(stores, list):
                return self.log_test("Store Data Structure", False, "Response is not a list")
            
            if len(stores) != 8:
                return self.log_test("Store Data Structure", False, f"Expected 8 stores, got {len(stores)}")
            
            # Verify each store has required fields
            required_fields = ['id', 'name', 'chain', 'address', 'latitude', 'longitude', 'distance_km', 'price_match_policy', 'logo_url']
            missing_fields = []
            
            for i, store in enumerate(stores):
                for field in required_fields:
                    if field not in store:
                        missing_fields.append(f"Store {i+1} missing '{field}'")
                
                # Check price match policy structure
                if 'price_match_policy' in store and isinstance(store['price_match_policy'], dict):
                    policy = store['price_match_policy']
                    if 'has_price_match' not in policy:
                        missing_fields.append(f"Store {i+1} price_match_policy missing 'has_price_match'")
            
            if missing_fields:
                return self.log_test("Store Data Structure", False, f"Missing fields: {', '.join(missing_fields[:3])}")
            
            # Verify store names match expected
            store_chains = [store.get('chain', '') for store in stores]
            found_chains = set(store_chains)
            expected_chains = set(expected_stores)
            
            if not expected_chains.issubset(found_chains):
                missing = expected_chains - found_chains
                return self.log_test("Store Data Structure", False, f"Missing expected chains: {missing}")
            
            return self.log_test("Store Data Structure", True, f"All 8 stores with correct structure returned")
            
        except Exception as e:
            return self.log_test("Store Data Structure", False, f"Error: {str(e)}")

    def run_comprehensive_test(self):
        """Run all tests for the location → stores flow"""
        print("🛒 SaleSavor Location → Stores Flow Test")
        print("Testing user-reported issue: Stores not populating after 'Get Location'")
        print("=" * 70)
        
        # Test 1: Basic connectivity
        print("\n1️⃣  BASIC CONNECTIVITY")
        connectivity_ok = self.test_api_connectivity()
        
        if not connectivity_ok:
            print("\n❌ Cannot proceed - API is not accessible")
            return False
        
        # Test 2: Basic stores/nearby functionality
        print("\n2️⃣  STORES/NEARBY BASIC FUNCTIONALITY")
        basic_ok = self.test_stores_nearby_basic()
        
        # Test 3: Timing and consistency
        print("\n3️⃣  TIMING AND CONSISTENCY")
        timing_ok = self.test_stores_nearby_timing()
        
        # Test 4: Edge cases
        print("\n4️⃣  EDGE CASES")
        edge_cases_ok = self.test_stores_nearby_edge_cases()
        
        # Test 5: Data structure validation
        print("\n5️⃣  DATA STRUCTURE VALIDATION")
        structure_ok = self.test_expected_store_data_structure()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        
        all_tests = [
            ("API Connectivity", connectivity_ok),
            ("Basic Functionality", basic_ok),
            ("Timing & Consistency", timing_ok),
            ("Edge Cases", edge_cases_ok),
            ("Data Structure", structure_ok)
        ]
        
        passed = sum(1 for _, success in all_tests if success)
        total = len(all_tests)
        
        for test_name, success in all_tests:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 LOCATION → STORES FLOW IS WORKING CORRECTLY")
            print("   • API responds quickly (< 10s)")
            print("   • Returns all 8 expected stores")
            print("   • Data structure is correct")
            print("   • Consistent across multiple requests")
            print("\n💡 If user still experiences issues, it may be:")
            print("   • Frontend state management issue")
            print("   • Browser/network specific problem")
            print("   • Timing issue in UI updates")
            return True
        else:
            print(f"\n⚠️  ISSUES DETECTED IN LOCATION → STORES FLOW")
            print("   Backend API has problems that could cause frontend issues")
            return False

def main():
    tester = LocationStoresFlowTester()
    success = tester.run_comprehensive_test()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())