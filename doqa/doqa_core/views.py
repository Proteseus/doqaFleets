from logging import log
from django.db.models.fields import Empty
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import folium

from .forms import VehicleForm, EmployeeForm, MaintenanceForm, TripsForm, InventoryForm
from .models import Vehicle, Employee, Maintenance, Trips, Inventory
from .getroute import get_route


def map(request):
    map_token = 'pk.eyJ1IjoiaG9ycmlibGVib2IxMSIsImEiOiJjbHNvZm42ZWEwYmViMmprNTRpaThvZ2ZhIn0.ROEbyxFl7m7I-7KNof8kMQ'
    # return render(request, 'map.html', {'mapbox_access_token': map_token})
    return render(request, 'showmap.html')

def showroute(request,lat1,long1,lat2,long2):
    figure = folium.Figure()
    lat1,long1,lat2,long2=float(lat1),float(long1),float(lat2),float(long2)
    route=get_route(long1,lat1,long2,lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                                 (route['start_point'][1])], 
                       zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure}
    return render(request,'showroute.html',context)

@login_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save(commit=True)
            return redirect('vehicle_list')  # Replace 'vehicle_list' with the actual URL or view name
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
            return redirect('employee_list')  # Replace 'vehicle_list' with the actual URL or view name
    else:
        form = EmployeeForm()

    return render(request, 'create_vehicle.html', {'form': form})

@login_required
def create_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('vehicle_detail')  # Replace 'vehicle_list' with the actual URL or view name
    else:
        form = MaintenanceForm()

    return render(request, 'create_vehicle.html', {'form': form})


@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('trip_list')  # Replace 'vehicle_list' with the actual URL or view name
    else:
        form = TripsForm()

    return render(request, 'create_vehicle.html', {'form': form})

@login_required
def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('inventory_list')  # Replace 'vehicle_list' with the actual URL or view name
    else:
        form = InventoryForm()

    return render(request, 'create_vehicle.html', {'form': form})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})
