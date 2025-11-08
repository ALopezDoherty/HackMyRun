from django.db import models

from django.contrib.auth.models import User

class SavedRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_address = models.TextField()
    target_distance_km = models.FloatField()
    generated_route_data = models.JSONField()  # Stores waypoints, distance, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.target_distance_km}km"

class RoutePreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_terrain = models.CharField(max_length=50, choices=[
        ('flat', 'Flat'),
        ('hilly', 'Hilly'),
        ('mixed', 'Mixed')
    ], default='mixed')
    avoid_busy_roads = models.BooleanField(default=True)
    include_parks = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
