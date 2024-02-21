from logging import log
from django.db.models.fields import Empty
from django.contrib.gis.geos import Point
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import folium

from .forms import VehicleForm, EmployeeForm, MaintenanceForm, TripsForm, InventoryForm
from .models import Vehicle, Employee, Maintenance, Trip, Inventory
from .getroute import get_route


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
    return render(request, 'map.html', context)

@login_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
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
