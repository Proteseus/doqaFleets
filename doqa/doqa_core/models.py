import uuid
from django.contrib.gis.db.models import PointField
from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration_number = models.CharField(max_length=20)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    current_location = PointField(null=True, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.registration_number

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    driver_license_number = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return self.name

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
    status = models.CharField(max_length=10)
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
    driver_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='trips')
    start_location = PointField()
    end_location = PointField()
    planned_start_time = models.DateTimeField()
    planned_end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, default='PENDING')
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


