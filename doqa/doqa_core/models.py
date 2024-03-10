import uuid
from datetime import date
from django.contrib.gis.db.models import PointField
from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    driver_license_number = models.CharField(max_length=20, unique=True)
    assigned = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration_number = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to ='uploads/vehicles/', null=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    driver_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    current_location = PointField(null=True, blank=True)
    fuel = models.FloatField(null=True, default=30)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.registration_number

    def get_latest_to_now_maintenance_date(self):
        today = date.today()

        # Get the closest pending maintenance date
        closest_pending_maintenance = Maintenance.objects.filter(vehicle=self).filter(
            scheduled_date__gte=today, status='PENDING'
        ).order_by("scheduled_date").first()

        # If there's a pending maintenance, return its scheduled date
        if closest_pending_maintenance:
            return closest_pending_maintenance.scheduled_date
        else:
            return None
        # Return the latest completed maintenance date
        return latest_completed_maintenance.completed_date if latest_completed_maintenance else None

    def get_last_to_now_maintenance_date(self):
        today = date.today()

         # If there's no pending maintenance, get the latest completed maintenance date
        latest_completed_maintenance = Maintenance.objects.filter(vehicle=self).filter(
            completed_date__lte=today
        ).order_by("-completed_date").first()

        # Return the latest completed maintenance date
        return latest_completed_maintenance.completed_date if latest_completed_maintenance else None

class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.vehicle

class Maintenance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = models.TextField()
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, default='PENDING')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.id


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.id


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_location_name = models.CharField()
    start_location = PointField()
    end_location_name = models.CharField()
    end_location = PointField()
    planned_start_time = models.DateTimeField()
    planned_end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, default='PENDING')
    route_data = models.JSONField(null=True, default=None)
    distance = models.FloatField(null=True, default=None)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.id


class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=20)
    last_restock_date = models.DateField()
    reorder_threshold = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.item_name


