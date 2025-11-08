from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .utils.route_generator import generate_run_routes
from .models import SavedRoute, RoutePreference, UserProfile, Badge, UserBadge

@csrf_exempt
@require_http_methods(["POST"])
def generate_routes_api(request):
    """HackMyRun API endpoint for generating routes"""
    try:
        # Check if content type is JSON
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)
        
        data = json.loads(request.body)
        start_address = data.get('start_address', '').strip()
        end_address = data.get('end_address', '').strip()
        distance = data.get('distance')
        mode = data.get('mode', 'endurance')
        is_loop = data.get('is_loop', False)
        
        # Validate inputs
        if not start_address:
            return JsonResponse({'error': 'Start address is required'}, status=400)
        
        if not is_loop and not end_address:
            return JsonResponse({'error': 'End address is required for point-to-point routes'}, status=400)
        
        try:
            distance = float(distance)
            if distance <= 0 or distance > 100:
                return JsonResponse({'error': 'Distance must be between 0.1 and 100 km'}, status=400)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Distance must be a valid number'}, status=400)
        
        # Validate mode
        if mode not in ['endurance', 'conditioning']:
            return JsonResponse({'error': 'Mode must be endurance or conditioning'}, status=400)
        
        # Generate routes
        routes = generate_run_routes(start_address, end_address, distance, mode, is_loop)
        
        return JsonResponse({
            'success': True,
            'routes': routes,
            'start_address': start_address,
            'end_address': end_address if not is_loop else None,
            'distance': distance,
            'mode': mode,
            'is_loop': is_loop
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
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)
        
        data = json.loads(request.body)
        
        # Create or get demo user (for hackathon - no real auth)
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='demo_user')
        
        # Validate required fields
        if not data.get('name') or not data.get('route_data'):
            return JsonResponse({'error': 'Route name and data are required'}, status=400)
        
        saved_route = SavedRoute.objects.create(
            user=user,
            name=data.get('name'),
            start_address=data.get('start_address', ''),
            end_address=data.get('end_address', ''),
            target_distance_km=data.get('distance', 0),
            generated_route_data=data.get('route_data'),
            is_loop=data.get('is_loop', False),
            route_mode=data.get('mode', 'endurance')
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
                'end_address': route.end_address,
                'distance': route.target_distance_km,
                'is_loop': route.is_loop,
                'mode': route.route_mode,
                'created_at': route.created_at.isoformat(),
                'route_data': route.generated_route_data
            })
        
        return JsonResponse({
            'success': True,
            'routes': routes_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# NEW: Gamification APIs
@require_http_methods(["GET"])
def leaderboard_api(request):
    """API endpoint for getting the leaderboard"""
    try:
        # Get top 10 users by total miles
        profiles = UserProfile.objects.all().order_by('-total_miles')[:10]
        
        leaderboard_data = []
        for rank, profile in enumerate(profiles, 1):
            leaderboard_data.append({
                'rank': rank,
                'username': profile.user.username,
                'total_miles': round(profile.total_miles, 1),
                'total_points': profile.total_points
            })
        
        return JsonResponse({
            'success': True,
            'leaderboard': leaderboard_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def record_run_api(request):
    """API endpoint for recording a completed run"""
    try:
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)
        
        data = json.loads(request.body)
        miles_run = data.get('miles', 0)
        
        if miles_run <= 0:
            return JsonResponse({'error': 'Miles must be positive'}, status=400)
        
        # For demo - use demo user
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='demo_user')
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update stats
        profile.update_stats(miles_run)
        
        return JsonResponse({
            'success': True,
            'message': f'Recorded {miles_run} miles',
            'total_miles': profile.total_miles,
            'total_points': profile.total_points
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def user_stats_api(request):
    """API endpoint for getting user statistics and badges"""
    try:
        # For demo - use demo user
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='demo_user')
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Get user badges
        user_badges = UserBadge.objects.filter(user=user).select_related('badge')
        badges_data = []
        for user_badge in user_badges:
            badges_data.append({
                'name': user_badge.badge.name,
                'miles_required': user_badge.badge.miles_required,
                'earned_date': user_badge.earned_date.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_miles': profile.total_miles,
                'total_points': profile.total_points,
                'username': user.username
            },
            'badges': badges_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)