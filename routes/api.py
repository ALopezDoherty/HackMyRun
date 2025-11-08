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