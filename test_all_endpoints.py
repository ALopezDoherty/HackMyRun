# test_all_endpoints.py - Test all possible endpoints
import requests

def test_endpoints():
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/",
        "/api/auth/login",
        "/auth/login", 
        "/api/login",
        "/login",
        "/api/user",
        "/api/users",
        "/user",
        "/users"
    ]
    
    print("Testing all endpoints...")
    
    for endpoint in endpoints:
        full_url = base_url + endpoint
        try:
            get_response = requests.get(full_url, timeout=5)
            print(f"GET {endpoint}: {get_response.status_code}")
            
            if "auth" in endpoint or "login" in endpoint:
                post_response = requests.post(full_url, json={}, timeout=5)
                print(f"POST {endpoint}: {post_response.status_code}")
                
        except Exception as e:
            print(f"ERROR {endpoint}: {e}")

if __name__ == "__main__":
    test_endpoints()