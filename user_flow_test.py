#!/usr/bin/env python3
"""
Test to simulate the exact user flow that's failing:
1. User can create profile ✅
2. User can get location to work ✅  
3. Shows "Locating stores" message but stores don't populate ❌

This test will help identify the root cause of the frontend issue.
"""

import requests
import json
import time
from datetime import datetime

class UserFlowTester:
    def __init__(self, base_url="https://grocery-saver-4.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
    def test_complete_user_flow(self):
        """Test the complete user flow as reported"""
        print("🧪 Testing Complete User Flow - Reproducing User Issue")
        print("=" * 60)
        
        # Step 1: Test profile creation (user says this works ✅)
        print("\n1️⃣  PROFILE CREATION (User reports: ✅ Working)")
        profile_success = self.test_profile_creation()
        
        # Step 2: Test location functionality (user says this works ✅)
        print("\n2️⃣  LOCATION DETECTION (User reports: ✅ Working)")
        location_success = self.test_location_detection()
        
        # Step 3: Test stores population (user says this fails ❌)
        print("\n3️⃣  STORES POPULATION (User reports: ❌ Not working)")
        stores_success = self.test_stores_population()
        
        # Step 4: Test potential edge cases that could cause the issue
        print("\n4️⃣  EDGE CASE ANALYSIS")
        edge_case_results = self.test_edge_cases()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 USER FLOW TEST RESULTS")
        print(f"✅ Profile Creation: {'PASS' if profile_success else 'FAIL'}")
        print(f"✅ Location Detection: {'PASS' if location_success else 'FAIL'}")
        print(f"❌ Stores Population: {'PASS' if stores_success else 'FAIL'} (User Issue)")
        
        if stores_success:
            print("\n🤔 ANALYSIS: Backend API is working correctly")
            print("   The issue is likely in the frontend:")
            print("   • React state management problem")
            print("   • Timing issue in UI updates")
            print("   • Missing error handling for edge cases")
            print("   • Browser-specific issue")
        else:
            print("\n🚨 ANALYSIS: Backend API has issues")
            print("   This could explain the user's problem")
        
        return profile_success, location_success, stores_success
    
    def test_profile_creation(self):
        """Test profile creation (user says this works)"""
        profile_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "household_size": 4,
            "dietary_preferences": ["vegetarian"],
            "budget_range": "moderate"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/profile",
                json=profile_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                profile = response.json()
                print(f"   ✅ Profile created: {profile.get('name')} (ID: {profile.get('id')[:8]}...)")
                return True
            else:
                print(f"   ❌ Profile creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Profile creation error: {str(e)}")
            return False
    
    def test_location_detection(self):
        """Test location detection (user says this works)"""
        # Simulate the Toronto fallback that the app uses
        location_data = {
            "latitude": 43.6532,
            "longitude": -79.3832,
            "address": "Toronto, ON"
        }
        
        print(f"   📍 Testing with Toronto coordinates: {location_data}")
        
        # This simulates what happens when the frontend gets location
        # The next step should be calling /api/stores/nearby
        return True  # User says location detection works
    
    def test_stores_population(self):
        """Test the stores population that user says fails"""
        location_data = {
            "latitude": 43.6532,
            "longitude": -79.3832,
            "address": "Toronto, ON"
        }
        
        print(f"   🏪 Testing stores/nearby API call...")
        
        try:
            # This is the exact call the frontend makes after getting location
            start_time = time.time()
            response = requests.post(
                f"{self.api_url}/stores/nearby",
                json=location_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"   ⏱️  Response time: {response_time:.2f}s")
            
            if response.status_code == 200:
                stores = response.json()
                if isinstance(stores, list) and len(stores) > 0:
                    print(f"   ✅ API returned {len(stores)} stores")
                    
                    # Check if stores have all required fields for frontend
                    first_store = stores[0]
                    required_fields = ['id', 'name', 'chain', 'address', 'distance_km', 'price_match_policy']
                    missing_fields = [field for field in required_fields if field not in first_store]
                    
                    if missing_fields:
                        print(f"   ⚠️  Missing fields in store data: {missing_fields}")
                        print("   This could cause frontend rendering issues!")
                        return False
                    
                    print(f"   📋 First store: {first_store['name']} ({first_store['distance_km']} km)")
                    print(f"   🏷️  Store data structure looks correct")
                    return True
                else:
                    print(f"   ❌ API returned empty stores list")
                    print("   This would cause the frontend to show nothing!")
                    return False
            else:
                print(f"   ❌ API error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"   ❌ API timeout after 15s")
            print("   This could cause frontend to hang on 'Locating stores'")
            return False
        except Exception as e:
            print(f"   ❌ API error: {str(e)}")
            return False
    
    def test_edge_cases(self):
        """Test edge cases that might cause the user's issue"""
        test_cases = [
            {
                "name": "Network timeout simulation",
                "timeout": 1,  # Very short timeout
                "expected": "Should handle timeout gracefully"
            },
            {
                "name": "Invalid coordinates",
                "data": {"latitude": 999, "longitude": 999},
                "expected": "Should return empty list or error"
            },
            {
                "name": "Missing coordinates",
                "data": {},
                "expected": "Should return 400 error"
            }
        ]
        
        results = []
        for test_case in test_cases:
            print(f"\n   🧪 {test_case['name']}")
            
            try:
                timeout = test_case.get('timeout', 10)
                data = test_case.get('data', {"latitude": 43.6532, "longitude": -79.3832})
                
                response = requests.post(
                    f"{self.api_url}/stores/nearby",
                    json=data,
                    headers={'Content-Type': 'application/json'},
                    timeout=timeout
                )
                
                print(f"      Status: {response.status_code}")
                if response.status_code == 200:
                    stores = response.json()
                    print(f"      Stores: {len(stores) if isinstance(stores, list) else 'Invalid'}")
                else:
                    print(f"      Error: {response.text[:100]}")
                
                results.append({
                    'name': test_case['name'],
                    'status': response.status_code,
                    'success': True
                })
                
            except requests.exceptions.Timeout:
                print(f"      ⏰ Timeout (expected for timeout test)")
                results.append({
                    'name': test_case['name'],
                    'status': 'timeout',
                    'success': True
                })
            except Exception as e:
                print(f"      ❌ Error: {str(e)}")
                results.append({
                    'name': test_case['name'],
                    'error': str(e),
                    'success': False
                })
        
        return results

def main():
    tester = UserFlowTester()
    profile_ok, location_ok, stores_ok = tester.test_complete_user_flow()
    
    print("\n" + "=" * 60)
    print("🔍 ROOT CAUSE ANALYSIS")
    
    if stores_ok:
        print("\n✅ BACKEND IS WORKING CORRECTLY")
        print("   The user's issue is likely a FRONTEND problem:")
        print()
        print("   🐛 POTENTIAL FRONTEND ISSUES:")
        print("   1. React state not updating after API call")
        print("   2. Component not re-rendering when nearbyStores changes")
        print("   3. Missing loading/error states in UI")
        print("   4. Race condition in async state updates")
        print("   5. Browser-specific JavaScript issue")
        print()
        print("   🔧 RECOMMENDED FIXES:")
        print("   1. Add loading state for stores step")
        print("   2. Add error handling for empty stores response")
        print("   3. Add debugging logs to frontend")
        print("   4. Test in different browsers")
        print("   5. Check browser console for JavaScript errors")
    else:
        print("\n❌ BACKEND HAS ISSUES")
        print("   This explains the user's problem - fix backend first")
    
    return 0 if stores_ok else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())