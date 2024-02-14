import uuid
from django.contrib.gis.db import models as gisModels
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # Add other user-related fields as needed

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration_number = models.CharField(max_length=20)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    current_location = gisModels.PointField(null=True, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    # Add other vehicle-related fields as needed

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    driver_license_number = models.CharField(max_length=20)
    # Add other employee-related fields as needed

class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=10)
    # Add other alert-related fields as needed

class Maintenance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = models.TextField()
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10)
    # Add other maintenance-related fields as needed

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    # Add other report-related fields as needed

class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = models.TextField()
    order_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10)
    # Add other order-related fields as needed

class Trips(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_location = gisModels.PointField()
    end_location = gisModels.PointField()
    planned_start_time = models.DateTimeField()
    planned_end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    driver_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=15)
    # Add other trip-related fields as needed

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=20)
    last_restock_date = models.DateField()
    reorder_threshold = models.IntegerField()
    # Add other inventory-related fields as needed

class VehicleAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    assignment_start_time = models.DateTimeField()
    assignment_end_time = models.DateTimeField(null=True, blank=True)
    # Add other vehicle assignment-related fields as needed

class OrderAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    assignment_start_time = models.DateTimeField()
    assignment_end_time = models.DateTimeField(null=True, blank=True)
    # Add other order assignment-related fields as needed

class TripAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    assignment_start_time = models.DateTimeField()
    assignment_end_time = models.DateTimeField(null=True, blank=True)
    # Add other trip assignment-related fields as needed
