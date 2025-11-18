# HackMyRun

A running route planner application that generates navigable routes with turn-by-turn directions. Built with Django and OpenRouteService API for accurate route planning and navigation.

## Features

- Street navigation using OpenRouteService API
- Turn-by-turn directions for running routes
- Support for loop routes and point-to-point navigation
- Live GPS tracking during running sessions
- Custom distance targets (1-100km)
- Terrain preferences (flat, hilly, mixed)
- Route saving and management
- User progress tracking

## Requirements

- Python 3.8 or higher
- Django 4.2 or higher
- OpenRouteService API key (free tier available)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hackmyrun.git
cd hackmyrun
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up the database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Obtain OpenRouteService API key:
   - Register at https://openrouteservice.org/
   - Add your API key to the .env file:
   ```
   OPENROUTE_API_KEY=your_api_key_here
   ```

7. Start the development server:
```bash
python manage.py runserver
```

Access the application at http://localhost:8000

## Project Structure

```
hackmyrun/
├── models.py                 # Database models
├── api.py                    # REST API endpoints
├── utils/
│   ├── real_route_generator.py    # Route generation logic
│   └── route_generator.py         # Legacy route generator
├── templates/
│   ├── dashboard.html        # Main application interface
│   └── map.html             # Map interface
└── static/
    └── css/                 # Stylesheets
```

## API Endpoints

### Route Management
- POST /api/generate-routes/ - Generate new running routes
- POST /api/save-route/ - Save route to user profile
- GET /api/saved-routes/ - Retrieve saved routes

### Navigation
- POST /api/start-navigation/ - Begin running session
- POST /api/update-position/ - Update user GPS position
- POST /api/next-instruction/ - Get next navigation instruction

### Example API Usage
```javascript
// Generate a route
fetch('/api/generate-routes/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        start_address: 'Central Park, New York',
        distance: 5.0,
        is_loop: true
    })
})
```

## Usage

1. Set starting location and route type (loop or point-to-point)
2. Configure distance and terrain preferences
3. Generate and review route options
4. Select preferred route and start navigation
5. Follow turn-by-turn directions during run

The application provides real-time position tracking and progress monitoring during navigation sessions.

## Technology Stack

### Backend
- Django 4.2 web framework
- PostgreSQL (configurable, SQLite for development)
- Geopy for geocoding and distance calculations
- OpenRouteService API for route generation

### Frontend
- Vanilla JavaScript
- Leaflet.js for interactive maps
- OpenStreetMap tiles
- Browser Geolocation API

## Configuration

Create a .env file with the following variables:

```ini
DEBUG=True
SECRET_KEY=your_django_secret_key
OPENROUTE_API_KEY=your_openrouteservice_key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Deployment

### Production Configuration

1. Set debug mode to false:
```python
DEBUG = False
```

2. Configure allowed hosts:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

3. Set up production database:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hackmyrun',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Collect static files:
```bash
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open a pull request

### Development Setup
```bash
pip install -r requirements-dev.txt
python manage.py test
flake8 .
```

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

- Bug Reports: GitHub Issues
- Feature Requests: GitHub Discussions
- Documentation: Project Wiki

## Acknowledgments

- OpenRouteService for routing API
- OpenStreetMap contributors for map data
- Leaflet.js for mapping functionality
- Django community for web framework
