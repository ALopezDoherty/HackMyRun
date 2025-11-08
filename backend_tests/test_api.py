import requests
import json
from config import BASE_URL

def test_backend_apis():
    """
    Comprehensive test script for Siress backend APIs
    """
    print('\n=== SIRESS BACKEND API TESTS ===\n')
    
    # Test 1: Authentication
    print('1. Testing Authentication...')
    auth_response = requests.post(f"{BASE_URL}/api/auth/login", 
                                 json={"email": "test@example.com", "password": "test123"})
    
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        token = auth_data.get('token', '')
        print(f'✓ Authentication SUCCESS - Token received')
    else:
        print(f'✗ Authentication FAILED: {auth_response.status_code}')
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test 2: User Profile
    print('\n2. Testing User Profile...')
    profile_response = requests.get(f"{BASE_URL}/api/user/profile", headers=headers)
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f'✓ Profile SUCCESS - User: {profile_data.get("username", "N/A")}')
    else:
        print(f'✗ Profile failed: {profile_response.status_code}')
    
    # Test 3: Route Planning
    print('\n3. Testing Route Planning...')
    route_payload = {
        "start": "40.7128,-74.0060",
        "end": "40.7282,-73.7942",
        "preferences": {"scenic": True, "elevation": "moderate"}
    }
    route_response = requests.post(f"{BASE_URL}/api/route/plan", 
                                  json=route_payload, headers=headers)
    
    if route_response.status_code == 200:
        route_data = route_response.json()
        routes_count = len(route_data.get('routes', []))
        print(f'✓ Route Planning SUCCESS - Generated {routes_count} routes')
    else:
        print(f'✗ Route Planning failed: {route_response.status_code}')
    
    # Test 4: Save Route
    print('\n4. Testing Save Route...')
    save_response = requests.post(f"{BASE_URL}/api/route/save", 
                                 json={"route_id": "test_route_123"}, headers=headers)
    
    if save_response.status_code == 200:
        print('✓ Save Route SUCCESS')
    else:
        print(f'✗ Save Route failed: {save_response.status_code}')
    
    # Test 5: Leaderboard
    print('\n5. Testing Leaderboard...')
    leaderboard_response = requests.get(f"{BASE_URL}/api/leaderboard", headers=headers)
    
    if leaderboard_response.status_code == 200:
        leaderboard_data = leaderboard_response.json()
        print(f'✓ Leaderboard SUCCESS - {len(leaderboard_data.get("users", []))} users')
    else:
        print(f'✗ Leaderboard failed: {leaderboard_response.status_code}')
    
    # Test 6: User Stats
    print('\n6. Testing User Stats...')
    stats_response = requests.get(f"{BASE_URL}/api/user-stats", headers=headers)
    
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
        total_miles = stats_data.get('stats', {}).get('total_miles', 0)
        badges_count = len(stats_data.get('badges', []))
        print(f'✓ User Stats: {total_miles} total miles')
        print(f'✓ Badges earned: {badges_count}')
    else:
        print(f'✗ User stats failed: {stats_response.status_code}')
    
    print('\n=== SIRESS TEST COMPLETE ===')

if __name__ == "__main__":
    test_backend_apis()