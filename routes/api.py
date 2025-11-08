from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .utils.route_generator import generate_run_routes
from .models import SavedRoute, RoutePreference

@csrf_exempt
@require_http_methods(["POST"])
def generate_routes_api(request):
    """HackMyRun API endpoint for generating routes"""
    try:
        # Check if content type is JSON
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)
        
        data = json.loads(request.body)
        address = data.get('address', '').strip()
        distance = data.get('distance')
        
        # Validate inputs
        if not address:
            return JsonResponse({'error': 'Address is required'}, status=400)
        
        try:
            distance = float(distance)
            if distance <= 0 or distance > 100:
                return JsonResponse({'error': 'Distance must be between 0.1 and 100 km'}, status=400)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Distance must be a valid number'}, status=400)
        
        # Generate routes
        routes = generate_run_routes(address, distance)
        
        return JsonResponse({
            'success': True,
            'routes': routes,
            'address': address,
            'distance': distance
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def save_route_api(request):
    """HackMyRun API endpoint for saving a route"""
    try:
        # Check if content type is JSON
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)
        
        data = json.loads(request.body)
        
        # Create or get demo user (for now no real auth)
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='demo_user')
        
        # Validate required fields
        if not data.get('name') or not data.get('route_data'):
            return JsonResponse({'error': 'Route name and data are required'}, status=400)
        
        saved_route = SavedRoute.objects.create(
            user=user,
            name=data.get('name'),
            start_address=data.get('start_address', ''),
            target_distance_km=data.get('distance', 0),
            generated_route_data=data.get('route_data')
        )
        
        return JsonResponse({
            'success': True,
            'route_id': saved_route.id,
            'message': 'Route saved successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_saved_routes_api(request):
    """HackMyRun API endpoint for retrieving saved routes"""
    try:
        # For demo - get routes for demo user
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='demo_user')
        
        saved_routes = SavedRoute.objects.filter(user=user).order_by('-created_at')
        
        routes_data = []
        for route in saved_routes:
            routes_data.append({
                'id': route.id,
                'name': route.name,
                'start_address': route.start_address,
                'distance': route.target_distance_km,
                'created_at': route.created_at.isoformat(),
                'route_data': route.generated_route_data
            })
        
        return JsonResponse({
            'success': True,
            'routes': routes_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)