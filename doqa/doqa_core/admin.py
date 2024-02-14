from django.contrib import admin
from .models import Vehicle, Employee, Maintenance, Trips, Inventory, Report, Alert

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'registration_number', 'make', 'model', 'year']
    # Add other configurations as needed

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact_number', 'driver_license_number']
    # Add other configurations as needed

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'description', 'scheduled_date', 'completed_date', 'status']
    # Add other configurations as needed

@admin.register(Trips)
class TripsAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'planned_start_time', 'planned_end_time', 'status']
    # Add other configurations as needed

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'item_name', 'quantity', 'unit_of_measurement', 'last_restock_date', 'reorder_threshold']
    # Add other configurations as needed

@admin.register(Report)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'report_type', 'value', 'timestamp']
    # Add other configurations as needed

@admin.register(Alert)
class AlertsAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'alert_type', 'timestamp', 'status']
    # Add other configurations as needed

