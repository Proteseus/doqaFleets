from django.urls import path
from .views import login_, logout_, dashboard, pre_route, get_options, result, coordinates, showroute, create_vehicle, create_employee, create_maintenance, create_trip, create_inventory, employee_list, vehicle_list, inventory_list, trips_list, trip_detail, edit_trip, delete_trip, delete_employee

urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', logout_, name='logout'),

    path('', dashboard, name='dashboard'),

    path('selectors/', pre_route, name='selectors'),
    
#    path('map/', map, name='map'),
    path('route/<str:lat1>,<str:long1>,<str:start_name>,<str:lat2>,<str:long2>,<str:end_name>/', showroute, name='showroute'),
    #path('showroute/<str:lat1>,<str:long1>,<str:lat2>,<str:long2>/', showroute, name='showroute_with_params'),
    # path('', showroute, name='showroute'),
    path('routed/<str:lat1>,<str:long1>,<str:lat2>,<str:long2>', showroute, name='showroute_updated'),

    path('register_vehicle/', create_vehicle, name='register_vehicle'), 
    path('vehicle_list/', vehicle_list, name='vehicle_list'),
    
    path('register_employee/', create_employee, name='register_employee'),
    path('employee_list/', employee_list, name='employee_list'),
    path('employee/<uuid:emp_id>/delete/', delete_employee, name='delete_employee'),
    
    path('register_maintenance/', create_maintenance, name='register_maintenance'),
    
    path('register_trip/', create_trip, name='register_trip'),
    path('trips_list/', trips_list, name='trips_list'),
    path('trip/<uuid:trip_id>/', trip_detail, name='trip_detail'),
    path('trip/<uuid:trip_id>/edit/', edit_trip, name='edit_trip'),
    path('trip/<uuid:trip_id>/delete/', delete_trip, name='delete_trip'),
    
    path('inventory_list/', inventory_list, name='inventory_list'),
]

htmx_patterns = [
    path('get_coord/', coordinates, name='get_coordinates'),
    path('get_options/', get_options, name='get_options'),
    path('results/', result, name='results'),

]

urlpatterns += htmx_patterns
