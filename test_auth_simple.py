# test_auth_simple.py - Simple authentication test
import requests
import json

def test_auth():
    url = "http://localhost:8000/api/auth/login"
    payload = {"email": "test@example.com", "password": "test123"}
    
    print("Testing login...")
    print(f"URL: {url}")
    print(f"Trying email: {payload['email']}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS: Login worked!")
            print(f"Response: {response.text}")
        elif response.status_code == 404:
            print("ERROR: Login page not found (404)")
            print("The /api/auth/login endpoint does not exist")
        elif response.status_code == 401:
            print("ERROR: Wrong username or password (401)")
        elif response.status_code == 500:
            print("ERROR: Server crashed (500) - check backend logs")
        else:
            print(f"UNKNOWN: Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server - make sure it's running!")
    except requests.exceptions.Timeout:
        print("ERROR: Server is not responding")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_auth()