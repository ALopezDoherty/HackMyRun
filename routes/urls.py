from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Route generation and management
    path('api/generate-routes/', api.generate_routes_api, name='api_generate_routes'),
    path('api/save-route/', api.save_route_api, name='api_save_route'),
    path('api/saved-routes/', api.get_saved_routes_api, name='api_saved_routes'),
    
    # Leaderboard & ranking endpoints
    path('api/leaderboard/', api.leaderboard_api, name='api_leaderboard'),
    path('api/record-run/', api.record_run_api, name='api_record_run'),
    path('api/user-stats/', api.user_stats_api, name='api_user_stats'),
]