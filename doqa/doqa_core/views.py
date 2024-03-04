from logging import log
import pprint
from django.db.models.fields import Empty
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

import folium

from .forms import LoginForm, VehicleForm, EmployeeForm, MaintenanceForm, TripsForm, EditTripsForm, InventoryForm
from .models import Vehicle, Employee, Maintenance, Trip, Inventory
from .utils import find_coordinates, get_route

########################################User Methods########################################

# User Login
def login_(request):
    if request.user.is_authenticated:
        return redirect('trips_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        #else:
            #messages.error(request, 'Invalid login credentials')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# User Logout
@login_required
def logout_(request):
    logout(request)
    return redirect('login')

########################################Dashboard########################################

# Dashboard view
@login_required
@cache_control(no_cache=True, must_revalidate=True)
def dashboard(request):
    vehicle_count = Vehicle.objects.count()
    employee_count = Employee.objects.count()
    maintenance_order_count = Maintenance.objects.count()
    trip_count = Trip.objects.filter(status='PENDING').count()

    trip_data = Trip.objects.all()

    context = {
        'vehicle_count': vehicle_count,
        'employee_count': employee_count,
        'maintenance_order_count': maintenance_order_count,
        'trip_count': trip_count,
        'trips': trip_data,
    }

    return render(request, 'dashboard.html', context)

########################################Trip Methods########################################

# get coordinates of locations
def coordinates(loc):
    if loc:
        coord = find_coordinates(loc)
        loc_title = coord['result'][0]
        point_val = f"{coord['result'][1]}, {coord['result'][2]}"
        return loc_title, point_val

# prepare to inject location options to the form in the UI
def get_options(request):
    if request.method == 'GET':
        for key in request.GET.keys():
            selector = request.GET.get(key)

            loc = coordinates(selector)
            options = []
            options.append({'label': loc[0], 'value': loc[1]})
            response_data = "\n".join([f'<option value="{option["value"]}, {option["label"]}">{option["label"]}</option>' for option in options])

        return HttpResponse(response_data)

# process given location and pass data to routed page
def result(request):
    route = ""
    for key in request.POST.keys():
        if key in ['start_location', 'end_location']:
            print(request.POST.get(key))
            route += request.POST.get(key).replace(" ", "")
            if key == 'start_location':
                route += ","
    coords = route.split(',')
    showroute_url = f'/route/{route}'
    return redirect('showroute', lat1=coords[0], long1=coords[1], start_name=coords[2], lat2=coords[3], long2=coords[4], end_name=coords[5])

# show partially filled form along with maped route data
@login_required
def showroute(request, lat1=None, long1=None, start_name=None, lat2=None, long2=None, end_name=None):
    figure = folium.Figure()
    if lat1 is not None:
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
        'start_location_name': start_name,
        'end_location_name': end_name
    }
    
    form = TripsForm(initial=initial_form_data)

    context = {'map': figure, 'form': form}
    return render(request, 'showroute.html', context)

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

    return redirect('trips_list')

@login_required
@cache_control(no_cache=True, must_revalidate=True)
def trips_list(request):
    trips = Trip.objects.all()
    return render(request, 'lists/trips_list.html', {'trips': trips})

@login_required
@cache_control(no_cache=True, must_revalidate=True)
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    driver = get_object_or_404(Employee, name=trip.vehicle.driver_id)
    vehicle = get_object_or_404(Vehicle, id=trip.vehicle.id)
    return render(request, 'details/trip_details.html', {'trip': trip, 'driver': driver, 'vehicle': vehicle})

@login_required
@cache_control(no_cache=True, must_revalidate=True)
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    if request.method == 'POST':
        form = EditTripsForm(request.POST, instance=trip)
        if form.is_valid():
            print(form.cleaned_data)
            up_trip = form.save(commit=True)
            up_trip.actual_start_time = form.cleaned_data['actual_start_time']
            up_trip.actual_end_time = form.cleaned_data['actual_end_time']
            up_trip.status = form.cleaned_data['status']
            up_trip.save()

            return redirect('trips_list')
    else:
        form = EditTripsForm(instance=trip)

    return render(request, 'edits/edit_trip.html', {'form': form, 'trip': trip})

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    trip.delete()
    return redirect('trips_list')

########################################Vehicle Methods########################################

@login_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            try:
                vehicle = form.save(commit=True)
                vehicle.created_by = request.user
                vehicle.save()
                return redirect('vehicle_list')
            except IntegrityError:
                form.add_error(None, "Error saving the vehicle. Please check the uniqueness of the fields.")
    else:
        form = VehicleForm()

    return render(request, 'lists/vehicle_list.html', {'form': form})

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    form = VehicleForm()
    return render(request, 'lists/vehicle_list.html', {'vehicles': vehicles, 'form': form})

@login_required
def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    driver = Employee.objects.filter(id=vehicle.driver_id_id)
    maintenance_orders = Maintenance.objects.filter(vehicle=vehicle_id)
    trips = Trip.objects.filter(vehicle=vehicle_id)

    form = MaintenanceForm()

    context = {
        'vehicle': vehicle,
        'driver': driver,
        'maintenance_orders': maintenance_orders,
        'trips': trips,
        'form': form
    }

    return render(request, 'details/vehicle_details.html', context)

def check_regitration_uniqueness(request):
    key = request.POST.get('registration_number')
    if Vehicle.objects.filter(registration_number=key).exists():
        return HttpResponse("Already registered")
    else:
        return HttpResponse("Not registred yet")

########################################Employee Methods########################################
@login_required
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save(commit=True)
            emp.created_by = request.user
            emp.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'lists/employee_list.html', {'form': form})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    form = EmployeeForm()
    return render(request, 'lists/employee_list.html', {'employees': employees, 'form': form})

@login_required
def employee_detail(request, driver_id):
    driver = get_object_or_404(Employee, id=driver_id)
    if Vehicle.objects.filter(driver_id=driver_id):
        vehicle = get_object_or_404(Vehicle, driver_id=driver_id)
        trips = Trip.objects.filter(vehicle=vehicle)

        context = {
            'driver': driver,
            'trips': trips,
        }
    else:
        context = {
            'driver': driver,
            'trips': []
        }
    return render(request, 'details/employee_details.html', context)

@login_required
def delete_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    emp.delete()
    return redirect('employee_list')

def check_contact_uniqueness(request):
    key = request.POST.get('contact_number')
    if Employee.objects.filter(contact_number=key).exists():
        return HttpResponse("Already registered")
    else:
        return HttpResponse("Not registred yet")

def check_license_uniqueness(request):
    key = request.POST.get('driver_license_number')
    if Employee.objects.filter(driver_license_number=key).exists():
        return HttpResponse("Already registered")
    else:
        return HttpResponse("Not registred yet")

########################################Maintenance Methods########################################

@login_required
def create_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            m_order = form.save(commit=True)
            m_order.created_by = request.user
            m_order.save()
            return redirect('vehicle_detail', form.cleaned_data['vehicle'].id)
    else:
        form = MaintenanceForm()

    return render(request, 'details/vehicle_details.html', {'form': form})

########################################Inventory Methods########################################

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, 'lists/inventory_list.html', {'inventory': inventories})

