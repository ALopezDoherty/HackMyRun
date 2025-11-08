from django.db import models
from django.contrib.auth.models import User

class SavedRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_address = models.TextField()
    end_address = models.TextField(blank=True, null=True)  # NEW: For point-to-point routes
    target_distance_km = models.FloatField()
    generated_route_data = models.JSONField()
    is_loop = models.BooleanField(default=False)  # NEW: Loop vs point-to-point
    route_mode = models.CharField(max_length=20, choices=[  # NEW: Endurance vs Conditioning
        ('endurance', 'Endurance (Flat)'),
        ('conditioning', 'Conditioning (Hilly)')
    ], default='endurance')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        route_type = "Loop" if self.is_loop else "Point-to-Point"
        return f"{self.name} - {self.target_distance_km}km ({route_type})"

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

# NEW: Models for gamification
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_miles = models.FloatField(default=0)
    total_points = models.IntegerField(default=0)
    
    def update_stats(self, miles_run):
        """Update user stats when they complete a run"""
        self.total_miles += miles_run
        self.total_points += int(miles_run)  # 1 point per mile
        self.save()
        
        # Check for new badges
        self.check_badges()
    
    def check_badges(self):
        """Check and award badges based on mileage"""
        badges = [
            (50, "50 Mile Club"),
            (150, "150 Mile Club"), 
            (300, "300 Mile Club")
        ]
        
        earned_badges = []
        for miles_required, badge_name in badges:
            if self.total_miles >= miles_required:
                badge, created = Badge.objects.get_or_create(
                    name=badge_name,
                    miles_required=miles_required
                )
                user_badge, created = UserBadge.objects.get_or_create(
                    user=self.user,
                    badge=badge
                )
                if created:
                    earned_badges.append(badge_name)
        
        return earned_badges
    
    def __str__(self):
        return f"{self.user.username} - {self.total_miles} miles"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    miles_required = models.IntegerField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.miles_required} miles)"

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"