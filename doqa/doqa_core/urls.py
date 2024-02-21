from django.urls import path
from .views import map, showroute, create_vehicle, create_employee, create_maintenance, create_trip, create_inventory, employee_list, vehicle_list, trips_list

urlpatterns = [
    path('map/', map, name='map'),
    path('route/', showroute, {'lat1': 8.950333, 'long1': 38.686444, 'lat2': 9.0180031, 'long2': 38.7977998}, name='showroute'),
    #path('showroute/<str:lat1>,<str:long1>,<str:lat2>,<str:long2>/', showroute, name='showroute_with_params'),
    # path('', showroute, name='showroute'),
    path('routed/<str:lat1>,<str:long1>,<str:lat2>,<str:long2>', showroute, name='showroute_updated'),

    path('register_vehicle/', create_vehicle, name='register_vehicle'), 
    path('vehicle_list/', vehicle_list, name='vehicle_list'),
    
    path('register_employee/', create_employee, name='register_employee'),
    path('employee_list/', employee_list, name='employee_list'),
    
    path('register_maintenance/', create_maintenance, name='register_maintenance'),
    
    path('register_trip/', create_trip, name='register_trip'),
    path('trips_list/', trips_list, name='trips_list'),

    path('register_inventory/', create_inventory, name='register_inventory'),
]
