from django import forms
from .models import Vehicle, Employee, Maintenance, Trips, Inventory

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

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
