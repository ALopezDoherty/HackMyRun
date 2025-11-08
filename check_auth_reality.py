# check_auth_reality.py - See what auth actually exists
import os
import requests

def check_backend_reality():
    print("=== AUTHENTICATION REALITY CHECK ===")
    
    # Check if auth files exist
    print("\n1. Checking for auth files in backend...")
    auth_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if any(keyword in file.lower() for keyword in ['auth', 'login', 'user']):
                auth_files.append(os.path.join(root, file))
    
    if auth_files:
        print("Found potential auth files:")
        for file in auth_files:
            print(f"  - {file}")
    else:
        print("NO AUTH FILES FOUND - Authentication probably doesn't exist")
    
    # Test what endpoints actually work
    print("\n2. Testing what endpoints respond...")
    base_url = "http://localhost:8000"
    test_endpoints = [
        "/", "/api/", "/auth/", "/login/", "/user/", "/users/",
        "/api/auth/login", "/auth/login", "/api/login", "/login"
    ]
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=3)
            print(f"  {endpoint}: {response.status_code}")
        except:
            print(f"  {endpoint}: FAILED")
    
    print("\n3. Checking database for users...")
    try:
        # Try to see if there's a users table in SQLite
        import sqlite3
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        user_tables = [table[0] for table in tables if 'user' in table[0].lower() or 'auth' in table[0].lower()]
        if user_tables:
            print(f"  Found user tables: {user_tables}")
        else:
            print("  NO USER TABLES IN DATABASE")
        conn.close()
    except Exception as e:
        print(f"  Could not check database: {e}")
    
    print("\n=== REALITY CHECK COMPLETE ===")

if __name__ == "__main__":
    check_backend_reality()