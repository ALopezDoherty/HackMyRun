from django.contrib import admin
from .models import SavedRoute, RoutePreference

@admin.register(SavedRoute)
class SavedRouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_address', 'target_distance_km', 'created_at']
    list_filter = ['created_at', 'user']

@admin.register(RoutePreference)
class RoutePreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_terrain', 'avoid_busy_roads', 'include_parks']
