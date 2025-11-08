# test_api.py
import requests
import json
from config import BASE_URL, ENDPOINTS

def test_backend_apis():
    """
    Test script for HackMyRun backend APIs
    """
    print('\n=== HACKMYRUN BACKEND API TESTS ===\n')
    
    # Test 1: Generate Routes
    print('1. Testing Route Generation...')
    route_payload = {
        "start_address": "Central Park, New York",
        "end_address": "Times Square, New York", 
        "distance": 5.0,
        "mode": "endurance",
        "is_loop": False
    }
    
    generate_response = requests.post(
        f"{BASE_URL}{ENDPOINTS['generate_routes']}", 
        json=route_payload
    )
    
    if generate_response.status_code == 200:
        route_data = generate_response.json()
        routes_count = len(route_data.get('routes', []))
        print(f'SUCCESS: Route Generation - Created {routes_count} routes')
        
        # Save first route for later tests
        if routes_count > 0:
            first_route = route_data['routes'][0]
    else:
        print(f'ERROR: Route Generation failed - {generate_response.status_code}')
        print(f'Response: {generate_response.text}')
        return
    
    # Test 2: Save Route
    print('\n2. Testing Save Route...')
    save_payload = {
        "name": "Test Run Route",
        "start_address": "Central Park, New York",
        "end_address": "Times Square, New York",
        "distance": 5.0,
        "is_loop": False,
        "mode": "endurance",
        "route_data": first_route
    }
    
    save_response = requests.post(
        f"{BASE_URL}{ENDPOINTS['save_route']}", 
        json=save_payload
    )
    
    if save_response.status_code == 200:
        save_data = save_response.json()
        print(f'SUCCESS: Save Route - ID: {save_data.get("route_id")}')
    else:
        print(f'ERROR: Save Route failed - {save_response.status_code}')
    
    # Test 3: Get Saved Routes
    print('\n3. Testing Get Saved Routes...')
    saved_response = requests.get(f"{BASE_URL}{ENDPOINTS['saved_routes']}")
    
    if saved_response.status_code == 200:
        saved_data = saved_response.json()
        routes_count = len(saved_data.get('routes', []))
        print(f'SUCCESS: Saved Routes - Found {routes_count} routes')
    else:
        print(f'ERROR: Saved Routes failed - {saved_response.status_code}')
    
    # Test 4: Leaderboard
    print('\n4. Testing Leaderboard...')
    leaderboard_response = requests.get(f"{BASE_URL}{ENDPOINTS['leaderboard']}")
    
    if leaderboard_response.status_code == 200:
        leaderboard_data = leaderboard_response.json()
        users_count = len(leaderboard_data.get('leaderboard', []))
        print(f'SUCCESS: Leaderboard - Found {users_count} users')
    else:
        print(f'ERROR: Leaderboard failed - {leaderboard_response.status_code}')
    
    # Test 5: Record a Run
    print('\n5. Testing Record Run...')
    record_payload = {
        "miles": 3.5
    }
    
    record_response = requests.post(
        f"{BASE_URL}{ENDPOINTS['record_run']}", 
        json=record_payload
    )
    
    if record_response.status_code == 200:
        record_data = record_response.json()
        print(f'SUCCESS: Record Run - {record_data.get("message")}')
    else:
        print(f'ERROR: Record Run failed - {record_response.status_code}')
    
    # Test 6: User Stats
    print('\n6. Testing User Stats...')
    stats_response = requests.get(f"{BASE_URL}{ENDPOINTS['user_stats']}")
    
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
        total_miles = stats_data.get('stats', {}).get('total_miles', 0)
        badges_count = len(stats_data.get('badges', []))
        print(f'SUCCESS: User Stats - {total_miles} total miles')
        print(f'SUCCESS: Badges earned - {badges_count}')
    else:
        print(f'ERROR: User stats failed - {stats_response.status_code}')
    
    print('\n=== TEST COMPLETE ===')

if __name__ == "__main__":
    test_backend_apis()