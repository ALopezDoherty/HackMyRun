import random
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class RouteGenerator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="hack_my_run")
    
    def generate_routes(self, start_address, end_address, target_distance_km, mode='endurance', is_loop=False, num_routes=3):
        """
        Generate running routes - supports both point-to-point and loop routes
        """
        try:
            # Geocode start address
            start_location = self.geolocator.geocode(start_address)
            if not start_location:
                return self._generate_fallback_routes(target_distance_km, num_routes, is_loop, mode)
            
            start_coords = (start_location.latitude, start_location.longitude)
            
            # For point-to-point routes, geocode end address
            end_coords = None
            if not is_loop and end_address:
                end_location = self.geolocator.geocode(end_address)
                if end_location:
                    end_coords = (end_location.latitude, end_location.longitude)
            
            routes = []
            for i in range(num_routes):
                if is_loop:
                    route = self._generate_loop_route(start_coords, target_distance_km, mode, i)
                else:
                    route = self._generate_point_to_point_route(start_coords, end_coords, target_distance_km, mode, i)
                routes.append(route)
            
            return routes
            
        except Exception as e:
            print(f"HackMyRun route generation error: {e}")
            return self._generate_fallback_routes(target_distance_km, num_routes, is_loop, mode)
    
    def _generate_loop_route(self, center_coords, distance_km, mode, route_index):
        """Generate a loop route that starts and ends at the same point"""
        center_lat, center_lng = center_coords
        
        # Adjust route characteristics based on mode
        if mode == 'endurance':
            # Flatter, more consistent routes
            elevation_gain = random.randint(5, 30)
            route_smoothness = 0.8  # Smoother curves
        else:  # conditioning
            # Hillier, more varied routes
            elevation_gain = random.randint(30, 100)
            route_smoothness = 0.5  # More variation
        
        waypoints = []
        points = 12
        
        for i in range(points + 1):
            angle = (i / points) * 2 * math.pi
            
            # Add variation based on mode
            variation = 1 + (route_index * 0.1 * route_smoothness)
            
            lat_offset = math.cos(angle * variation) * (distance_km / 15)
            lng_offset = math.sin(angle * variation) * (distance_km / 15)
            
            lat = center_lat + lat_offset
            lng = center_lng + lng_offset
            waypoints.append([round(lat, 6), round(lng, 6)])
        
        # Close the loop
        waypoints.append(waypoints[0])
        
        return {
            'id': route_index,
            'name': f'Loop Route {route_index + 1}',
            'distance': round(distance_km * random.uniform(0.9, 1.1), 1),
            'description': self._get_loop_description(route_index, mode),
            'difficulty': self._get_difficulty(route_index, mode),
            'waypoints': waypoints,
            'elevation_gain': elevation_gain,
            'estimated_time': f"{int(distance_km * 6)}-{int(distance_km * 8)} min",
            'terrain': self._get_terrain_type(route_index, mode),
            'is_loop': True,
            'mode': mode,
            'start_lat': center_lat,
            'start_lng': center_lng
        }
    
    def _generate_point_to_point_route(self, start_coords, end_coords, distance_km, mode, route_index):
        """Generate a point-to-point route from start to end coordinates"""
        start_lat, start_lng = start_coords
        
        if end_coords:
            end_lat, end_lng = end_coords
            # Calculate direct distance and adjust waypoints accordingly
            direct_distance = geodesic(start_coords, end_coords).km
            adjusted_distance = max(distance_km, direct_distance * 1.2)
        else:
            # If no end address provided, generate a semi-random end point
            end_lat = start_lat + (distance_km / 15) * random.uniform(-1, 1)
            end_lng = start_lng + (distance_km / 15) * random.uniform(-1, 1)
            adjusted_distance = distance_km
        
        # Adjust route based on mode
        if mode == 'endurance':
            elevation_gain = random.randint(10, 40)
            complexity = 0.3  # Straighter routes
        else:  # conditioning
            elevation_gain = random.randint(40, 120)
            complexity = 0.7  # More winding routes
        
        waypoints = []
        points = 8
        
        # Start point
        waypoints.append([start_lat, start_lng])
        
        # Intermediate points with variation based on mode
        for i in range(1, points):
            progress = i / points
            base_lat = start_lat + (end_lat - start_lat) * progress
            base_lng = start_lng + (end_lng - start_lng) * progress
            
            # Add variation based on mode and complexity
            lat_variation = math.sin(progress * math.pi * complexity) * (adjusted_distance / 20)
            lng_variation = math.cos(progress * math.pi * complexity) * (adjusted_distance / 20)
            
            lat = base_lat + lat_variation * random.uniform(-1, 1)
            lng = base_lng + lng_variation * random.uniform(-1, 1)
            
            waypoints.append([round(lat, 6), round(lng, 6)])
        
        # End point
        waypoints.append([end_lat, end_lng])
        
        actual_distance = adjusted_distance * random.uniform(0.9, 1.1)
        
        return {
            'id': route_index,
            'name': f'Point-to-Point Route {route_index + 1}',
            'distance': round(actual_distance, 1),
            'description': self._get_point_to_point_description(route_index, mode),
            'difficulty': self._get_difficulty(route_index, mode),
            'waypoints': waypoints,
            'elevation_gain': elevation_gain,
            'estimated_time': f"{int(actual_distance * 6)}-{int(actual_distance * 8)} min",
            'terrain': self._get_terrain_type(route_index, mode),
            'is_loop': False,
            'mode': mode,
            'start_lat': start_lat,
            'start_lng': start_lng,
            'end_lat': end_lat,
            'end_lng': end_lng
        }
    
    def _get_loop_description(self, index, mode):
        base_descriptions = [
            "Scenic loop with beautiful views",
            "Perfect training circuit",
            "Well-balanced loop route",
            "Challenging circular course"
        ]
        mode_specific = " and gentle hills" if mode == 'endurance' else " with varied elevation"
        return base_descriptions[index % len(base_descriptions)] + mode_specific
    
    def _get_point_to_point_description(self, index, mode):
        base_descriptions = [
            "Direct route with efficient path",
            "Adventure from start to finish", 
            "Progressive running journey",
            "Destination-focused route"
        ]
        mode_specific = ", mostly flat terrain" if mode == 'endurance' else ", challenging hills"
        return base_descriptions[index % len(base_descriptions)] + mode_specific
    
    def _get_difficulty(self, index, mode):
        if mode == 'endurance':
            difficulties = ['Easy', 'Moderate']
        else:  # conditioning
            difficulties = ['Moderate', 'Challenging']
        return difficulties[index % len(difficulties)]
    
    def _get_terrain_type(self, index, mode):
        if mode == 'endurance':
            terrains = ['Paved', 'Mixed', 'Smooth Trail']
        else:  # conditioning
            terrains = ['Mixed', 'Trail', 'Varied']
        return terrains[index % len(terrains)]
    
    def _generate_fallback_routes(self, distance_km, num_routes, is_loop, mode):
        """Generate fallback routes when geocoding fails"""
        center_coords = (40.7128, -74.0060)  # NYC coordinates as fallback
        routes = []
        
        for i in range(num_routes):
            if is_loop:
                route = self._generate_loop_route(center_coords, distance_km, mode, i)
            else:
                end_coords = (40.7128 + random.uniform(-0.1, 0.1), -74.0060 + random.uniform(-0.1, 0.1))
                route = self._generate_point_to_point_route(center_coords, end_coords, distance_km, mode, i)
            routes.append(route)
        
        return routes

def generate_run_routes(start_address, end_address, distance_km, mode='endurance', is_loop=False):
    generator = RouteGenerator()
    return generator.generate_routes(start_address, end_address, distance_km, mode, is_loop)