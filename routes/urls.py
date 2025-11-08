from django.contrib import admin
from django.urls import path, include
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),

    path('api/generate-routes/', api.generate_routes_api, name='api_generate_routes'),
    path('api/save-route/', api.save_route_api, name='api_save_route'),
    path('api/saved-routes/', api.get_saved_routes_api, name='api_saved_routes'),
]