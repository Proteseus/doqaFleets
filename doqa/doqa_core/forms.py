from datetime import timedelta
from django import forms
from django.utils.http import formatdate
from .models import Vehicle, Employee, Maintenance, Trip, Inventory
from django.contrib.gis.forms import PointField
from django.contrib.gis.geos import Point
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )

class VehicleForm(forms.ModelForm):
    next_maintenance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'make', 'model', 'year', 'next_maintenance_date', 'driver_id']

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)

        # Override the queryset for the driver_id field
        unassigned_employees = Employee.objects.filter(assigned=False)
        self.fields['driver_id'].queryset = unassigned_employees

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'driver_license_number', 'contact_number']

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['vehicle', 'description', 'scheduled_date', 'status']
        widgets = {
                'vehicle': forms.TextInput(),
                'scheduled_date': forms.DateInput(attrs={'type': 'date'})
                }

class TripsForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'planned_start_time', 'planned_end_time', 'start_location', 'end_location', 'start_location_name', 'end_location_name', 'route_data', 'distance']
        widgets = {
            'planned_start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'planned_end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'start_location': forms.TextInput(attrs={'type': 'location-input'}),
            'end_location': forms.TextInput(attrs={'type': 'location-input'}),
            'start_location_name': forms.TextInput(attrs={'type': 'location-input'}),
            'end_location_name': forms.TextInput(attrs={'type': 'location-input'}),
        }

    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select())
    actual_start_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    actual_end_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


    def __init__(self, *args, **kwargs):
        super(TripsForm, self).__init__(*args, **kwargs)


    def clean_start_location(self):
        start_location_str = self.cleaned_data['start_location']
        return self.parse_point(start_location_str)

    def clean_end_location(self):
        end_location_str = self.cleaned_data['end_location']
        return self.parse_point(end_location_str)

    def parse_point(self, point_str):
        try:
            #print(str(point_str[0]))
            lat = point_str[0]
            lon = point_str[1]
            #point = Point(lon, lat)
            print(lon, lat, sep=',')
            return point_str  # Note: Point takes longitude first, then latitude
        except (ValueError, IndexError):
            raise forms.ValidationError("Invalid input format. Use 'lat,long'.")

class EditTripsForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'planned_start_time', 'planned_end_time', 'start_location', 'end_location', 'start_location_name', 'end_location_name', 'route_data', 'distance']
        widgets = {
            'planned_start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'planned_end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'start_location': forms.TextInput(attrs={'type': 'location-input'}),
            'end_location': forms.TextInput(attrs={'type': 'location-input'}),
            'start_location_name': forms.TextInput(attrs={'type': 'location-input'}),
            'end_location_name': forms.TextInput(attrs={'type': 'location-input'}),
            'vehicle': forms.TextInput()
        }

    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select())
    actual_start_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    actual_end_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

