# setup_tests.ps1 - Complete setup script for backend tests

Write-Host " Setting up Siress Backend Test Environment..." -ForegroundColor Green

# Create results folder
if (!(Test-Path "results")) {
    New-Item -Path "results" -ItemType Directory
    Write-Host "✓ Created results folder" -ForegroundColor Green
}

# Create all required files
$files = @("config.py", "test_api.py", "run_tests.py", "requirements.txt", "__init__.py")

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -Path $file -ItemType File
        Write-Host " Created $file" -ForegroundColor Green
    }
    else {
        Write-Host " $file already exists" -ForegroundColor Yellow
    }
}

# Write content to config.py
@"
# Configuration for backend tests
BASE_URL = "http://localhost:8000"  # Adjust to your backend URL

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
"@ | Out-File -FilePath config.py -Encoding utf8

# Write content to requirements.txt
@"
requests>=2.28.0
python-dotenv>=0.19.0
pytest>=7.0.0
"@ | Out-File -FilePath requirements.txt -Encoding utf8

Write-Host "`n Basic file structure created!" -ForegroundColor Green
Write-Host " Now manually copy the content for test_api.py and run_tests.py" -ForegroundColor Yellow