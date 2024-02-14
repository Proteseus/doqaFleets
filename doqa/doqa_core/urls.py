from django.urls import path
from .views import MarkersMapView, create_vehicle, create_employee, create_maintenance, create_trip, create_inventory, employee_list

urlpatterns = [
    path('map/', MarkersMapView.as_view(), name='map'),
    path('register_vehicle/', create_vehicle, name='register_vehicle'),
    path('register_employee/', create_employee, name='register_employee'),
    path('register_maintenance/', create_maintenance, name='register_maintenance'),
    path('register_trip/', create_trip, name='register_trip'),
    path('register_inventory/', create_inventory, name='register_inventory'),
    path('employee-list/', employee_list, name='employee_list'),
]
