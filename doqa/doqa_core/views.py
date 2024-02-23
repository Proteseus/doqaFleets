from logging import log
import pprint
from django.db.models.fields import Empty
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import folium

from .forms import LoginForm, VehicleForm, EmployeeForm, MaintenanceForm, TripsForm, InventoryForm
from .models import Vehicle, Employee, Maintenance, Trip, Inventory
from .getroute import get_route
from .utils import find_coordinates

def login_(request):
    if request.user.is_authenticated:
        return redirect('trips_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def dashboard(request):
    vehicle_count = Vehicle.objects.count()
    employee_count = Employee.objects.count()
    maintenance_order_count = Maintenance.objects.count()
    trip_count = Trip.objects.count()

    inventory_data = Inventory.objects.all()

    context = {
        'vehicle_count': vehicle_count,
        'employee_count': employee_count,
        'maintenance_order_count': maintenance_order_count,
        'trip_count': trip_count,
        'inventory_data': inventory_data,
    }

    return render(request, 'dashboard.html', context)

def map(request):
    map_token = 'pk.eyJ1IjoiaG9ycmlibGVib2IxMSIsImEiOiJjbHNvZm42ZWEwYmViMmprNTRpaThvZ2ZhIn0.ROEbyxFl7m7I-7KNof8kMQ'
    # return render(request, 'map.html', {'mapbox_access_token': map_token})
    return render(request, 'showmap.html')

def showroute(request, lat1='default_lat1', long1='default_long1', lat2='default_lat2', long2='default_long2'):
    figure = folium.Figure()
    lat1, long1, lat2, long2 = float(lat1), float(long1), float(lat2), float(long2)
    route = get_route(long1, lat1, long2, lat2)
    # print("\n#ROUTE: ", route) 
    m = folium.Map(location=[route['start_point'][0], route['start_point'][1]], zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='blue')).add_to(m)
    folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)
    
    figure.render()
    
    # Initialize the form with the map data
    initial_form_data = {
        'start_location': Point(route['start_point'][1], route['start_point'][0]),
        'end_location': Point(route['end_point'][1], route['end_point'][0]),
    }
    
    form = TripsForm(initial=initial_form_data)

    context = {'map': figure, 'form': form}
    return render(request, 'showroute.html', context)

def coordinates(request):
    if request.method == 'POST':
        pprint.pprint(request, indent=4)
        loc = request.POST.get('faux_start')
        pprint.pprint(loc)
        if loc:
            coord = find_coordinates(loc)
            point_val = f"POINT({coord['result'][0]} {coord['result'][1]})"
            print(point_val)
            return HttpResponse(point_val)
        else:
            return JsonResponse({'error': 'Missing location parameter'}, status=400)
    else:
        # Return an error response for non-GET requests
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=True)
            vehicle.created_by = request.user
            vehicle.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()

    return render(request, 'create_vehicle.html', {'form': form})

@login_required
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.created_by = request.user
            emp.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'create_employee.html', {'form': form})

@login_required
def create_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('vehicle_detail')
    else:
        form = MaintenanceForm()

    return render(request, 'create_vehicle.html', {'form': form})


@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['start_location'])
            trip = form.save(commit=True)
            trip.created_by = request.user
            trip.save()
            return redirect('trips_list')
    else:
        form = TripsForm()

    return redirect('showroute')

@login_required
def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()

    return render(request, 'create_vehicle.html', {'form': form})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'lists/employee_list.html', {'employees': employees})

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'lists/vehicle_list.html', {'vehicles': vehicles}
                  )
@login_required
def trips_list(request):
    trips = Trip.objects.all()
    return render(request, 'lists/trips_list.html', {'trips': trips})

@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    return render(request, 'details/trip_details.html', {'trip': trip})

@login_required
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    if request.method == 'POST':
        form = TripsForm(request.POST, instance=trip)
        if form.is_valid():
            print(form.cleaned_data)
            up_trip = form.save(commit=True)
            up_trip.actual_start_time = form.cleaned_data['actual_start_time']
            up_trip.actual_end_time = form.cleaned_data['actual_end_time']
            up_trip.status = form.cleaned_data['status']
            up_trip.save()
            
            return redirect('trips_list')
    else:
        form = TripsForm(instance=trip)

    return render(request, 'edits/edit_trip.html', {'form': form, 'trip': trip})

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    trip.delete()
    return redirect('trips_list')

@login_required
def delete_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    emp.delete()
    return redirect('employee_list')

