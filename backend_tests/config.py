import os

# Configuration for backend tests
BASE_URL = "http://localhost:8000"  

# Test credentials
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test123"

# API endpoints
ENDPOINTS = {
    "auth": "/api/auth/login",
    "profile": "/api/user/profile", 
    "route_plan": "/api/route/plan",
    "route_save": "/api/route/save",
    "leaderboard": "/api/leaderboard",
    "user_stats": "/api/user-stats"
}