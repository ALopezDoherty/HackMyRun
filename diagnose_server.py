# diagnose_server.py - Comprehensive server diagnosis
import requests

def diagnose_server():
    print("=== SERVER DIAGNOSIS ===")
    base_url = "http://localhost:8000"
    print(f"Target URL: {base_url}")
    
    # Test 1: Basic connectivity
    print("\n1. Testing basic connectivity...")
    try:
        response = requests.get(base_url, timeout=5)
        print(f"   SUCCESS: Connected to server - Status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Cannot connect - {e}")
        return False
    
    # Test 2: Check if API endpoints exist
    print("\n2. Testing API endpoints...")
    endpoints = [
        "/api/auth/login",
        "/auth/login", 
        "/api/login",
        "/login",
        "/api/user",
        "/api/users"
    ]
    
    for endpoint in endpoints:
        full_url = base_url + endpoint
        try:
            if "auth" in endpoint or "login" in endpoint:
                response = requests.post(full_url, json={}, timeout=5)
                print(f"   {endpoint}: POST - Status: {response.status_code}")
            else:
                response = requests.get(full_url, timeout=5)
                print(f"   {endpoint}: GET - Status: {response.status_code}")
        except Exception as e:
            print(f"   ERROR {endpoint}: {e}")
    
    print("\n=== DIAGNOSIS COMPLETE ===")

if __name__ == "__main__":
    diagnose_server()