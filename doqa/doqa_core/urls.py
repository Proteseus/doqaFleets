from django.urls import path
from .views import login_, logout_, dashboard, get_options, result, coordinates, showroute, create_vehicle, create_employee, employee_detail, create_maintenance, complete_maintenance, create_trip, check_available_vehicles, employee_list, vehicle_list, vehicle_detail, inventory_list, trips_list, trip_detail, edit_trip, delete_trip, delete_employee, check_contact_uniqueness, check_license_uniqueness, check_regitration_uniqueness, generate_reports

urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', logout_, name='logout'),
    path('', dashboard, name='dashboard'),
    path('route/<str:lat1>,<str:long1>,<str:start_name>,<str:lat2>,<str:long2>,<str:end_name>/', showroute, name='showroute'),
    path('routed/<str:lat1>,<str:long1>,<str:lat2>,<str:long2>', showroute, name='showroute_updated'),
    path('register_vehicle/', create_vehicle, name='register_vehicle'), 
    path('vehicle_list/', vehicle_list, name='vehicle_list'),
    path('vehicle/<uuid:vehicle_id>/', vehicle_detail, name='vehicle_detail'),
    path('register_employee/', create_employee, name='register_employee'),
    path('employee_list/', employee_list, name='employee_list'),
    path('employee/<uuid:driver_id>/', employee_detail, name='employee_detail'),
    path('employee/<uuid:emp_id>/delete/', delete_employee, name='delete_employee'),
    path('register_maintenance/', create_maintenance, name='register_maintenance'),
    path('complete_maintenance/<uuid:m_order_id>,<uuid:vehicle_id>', complete_maintenance, name='complete_maintenance'),
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
    path('check_contact_uniqueness/', check_contact_uniqueness, name='check_contact_uniqueness'),
    path('check_license_uniqueness/', check_license_uniqueness, name='check_license_uniqueness'),
    path('check_regitration_uniqueness/', check_regitration_uniqueness, name='check_regitration_uniqueness'),
    path('check_available_vehicles/', check_available_vehicles, name='check_available_vehicles'),
    path('generate_reports/', generate_reports, name='generate_reports'),

]

urlpatterns += htmx_patterns
