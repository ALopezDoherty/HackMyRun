import random
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class RouteGenerator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="Hack_My_Run")
    
    def generate_routes(self, start_address, target_distance_km, num_routes=3):
        """
        Generate running routes from a starting address
        Returns structured data for frontend
        """
        try:
            # Try to geocode the address
            location = self.geolocator.geocode(start_address)
            if location:
                center_lat, center_lng = location.latitude, location.longitude
            else:
                # Fallback to mock coordinates
                center_lat, center_lng = 40.7128, -74.0060  # NYC
                
            routes = []
            for i in range(num_routes):
                route = self._generate_structured_route(
                    center_lat, center_lng, target_distance_km, i
                )
                routes.append(route)
            
            return routes
            
        except Exception as e:
            print(f"Error in route generation: {e}")
            return self._generate_fallback_routes(target_distance_km, num_routes)
    
    def _generate_structured_route(self, center_lat, center_lng, distance_km, route_index):
        """Generate a structured route with realistic data"""
        waypoints = self._calculate_waypoints(center_lat, center_lng, distance_km, route_index)
        
        return {
            'id': route_index,
            'name': f'Route {route_index + 1}',
            'distance': round(distance_km * random.uniform(0.9, 1.1), 1),
            'description': self._get_route_description(route_index),
            'difficulty': self._get_difficulty(route_index),
            'waypoints': waypoints,
            'elevation_gain': random.randint(10, 100),  # meters
            'estimated_time': f"{int(distance_km * 6)}-{int(distance_km * 8)} min",  # running pace
            'terrain': self._get_terrain_type(route_index),
            'center_lat': center_lat,
            'center_lng': center_lng
        }
    
    def _calculate_waypoints(self, center_lat, center_lng, distance_km, route_index):
        """Calculate waypoints for a circular/loop route"""
        waypoints = []
        points = 12  # More points for smoother route
        
        # Different patterns for different routes
        patterns = ['circle', 'square', 'figure8']
        pattern = patterns[route_index % len(patterns)]
        
        for i in range(points + 1):
            angle = (i / points) * 2 * math.pi
            
            if pattern == 'circle':
                lat_offset = math.cos(angle) * (distance_km / 15)
                lng_offset = math.sin(angle) * (distance_km / 15)
            elif pattern == 'square':
                lat_offset = math.cos(angle) * (distance_km / 12) * (1 + 0.2 * math.sin(4 * angle))
                lng_offset = math.sin(angle) * (distance_km / 12) * (1 + 0.2 * math.cos(4 * angle))
            else:  # figure8
                lat_offset = math.sin(angle) * (distance_km / 15)
                lng_offset = math.sin(2 * angle) * (distance_km / 20)
            
            lat = center_lat + lat_offset
            lng = center_lng + lng_offset
            waypoints.append([round(lat, 6), round(lng, 6)])
        
        # Close the loop
        waypoints.append(waypoints[0])
        return waypoints
    
    def _get_route_description(self, index):
        descriptions = [
            "Scenic loop with park views and gentle hills",
            "Urban exploration passing local landmarks",
            "Quiet neighborhood streets with minimal traffic",
            "Mixed terrain through parks and residential areas",
            "Riverfront path with beautiful water views",
            "Historic district with architectural highlights"
        ]
        return descriptions[index % len(descriptions)]
    
    def _get_difficulty(self, index):
        difficulties = ['Easy', 'Moderate', 'Challenging']
        return difficulties[index % len(difficulties)]
    
    def _get_terrain_type(self, index):
        terrains = ['Paved', 'Mixed', 'Trail', 'Urban']
        return terrains[index % len(terrains)]
    
    def _generate_fallback_routes(self, distance_km, num_routes):
        """Generate fallback routes when geocoding fails"""
        return [self._generate_structured_route(40.7128, -74.0060, distance_km, i) 
                for i in range(num_routes)]

def generate_run_routes(address, distance_km):
    generator = RouteGenerator()
    return generator.generate_routes(address, distance_km)