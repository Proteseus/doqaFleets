from logging import log
from django.db.models.fields import Empty
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VehicleForm, EmployeeForm, MaintenanceForm, TripsForm, InventoryForm
from .models import Vehicle, Employee, Maintenance, Trips, Inventory

from django.views.generic.base import (
    TemplateView,
)

class MarkersMapView(TemplateView):
    template_name = "map.html"

def map(request):
    return render(request, 'map.html')

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
