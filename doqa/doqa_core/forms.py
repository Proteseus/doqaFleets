from django import forms
from .models import Vehicle, Employee, Maintenance, Trips, Inventory
from django.contrib.gis.forms import PointField

class VehicleForm(forms.ModelForm):
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
        model = Trips
        fields = '__all__'

    start_location = PointField(widget=forms.TextInput(attrs={'class': 'location-input'}))
    end_location = PointField(widget=forms.TextInput(attrs={'class': 'location-input'}))

    # Set default values for status and leave actual_times nullable
    status = forms.CharField(initial='Pending', widget=forms.HiddenInput())
    actual_start_time = forms.DateTimeField(required=False, widget=forms.HiddenInput())
    actual_end_time = forms.DateTimeField(required=False, widget=forms.HiddenInput())

    # Use TimeInput widget for planned times
    planned_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'datetime-local'}))
    planned_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'datetime-local'}))

    def __init__(self, *args, **kwargs):
        super(TripsForm, self).__init__(*args, **kwargs)

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
