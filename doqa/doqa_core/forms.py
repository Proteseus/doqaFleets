from django import forms
from .models import Vehicle, Employee, Maintenance, Trip, Inventory
from django.contrib.gis.forms import PointField
from django.contrib.gis.geos import Point

class VehicleForm(forms.ModelForm):
    last_maintenance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    next_maintenance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Vehicle
        fields = '__all__' 

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'

class TripsForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'driver_id', 'planned_start_time', 'planned_end_time', 'start_location', 'end_location']
        widgets = {
            'planned_start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'planned_end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'start_location': forms.TextInput(attrs={'type': 'location-input'}),
            'end_location': forms.TextInput(attrs={'type': 'location-input'}),
        }

    def clean_start_location(self):
        start_location_str = self.cleaned_data['start_location']
        return self.parse_point(start_location_str)

    def clean_end_location(self):
        end_location_str = self.cleaned_data['end_location']
        return self.parse_point(end_location_str)

    def parse_point(self, point_str):
        try:
            print(point_str)
            #lat, lon = map(float, point_str.split(','))
            #point = Point(lon, lat)
            #print(point)
            return point_str  # Note: Point takes longitude first, then latitude
        except (ValueError, IndexError):
            raise forms.ValidationError("Invalid input format. Use 'lat,long'.")
    # start_location = PointField(widget=forms.TextInput(attrs={'class': 'location-input'}))
    # end_location = PointField(widget=forms.TextInput(attrs={'class': 'location-input'}))

    # Set default values for status and leave actual_times nullable
    # status = forms.CharField(initial='Pending', widget=forms.HiddenInput())
    # actual_start_time = forms.DateTimeField(required=False, widget=forms.HiddenInput())
    # actual_end_time = forms.DateTimeField(required=False, widget=forms.HiddenInput())

    # Use TimeInput widget for planned times
    #planned_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'datetime-local'}))
    #planned_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'datetime-local'}))

    # def __init__(self, *args, **kwargs):
        # super(TripsForm, self).__init__(*args, **kwargs)

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
