from django import forms 
from .models import Employee

class SingleCalculationForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label=None, required=True, label='Select Employee')
    project_rate = forms.DecimalField(decimal_places=2, required=True, label='Enter Project Rate $')

class ExtraEmployeeForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label=None, required=True, label='Select Employee')
    project_rate = forms.DecimalField(decimal_places=2, required=True, label='Enter Project Rate $')
    hours = forms.DecimalField(decimal_places=2, max_value=40, required=True, label='Hours per Week on Project')
    extra_time = forms.ChoiceField(required=True, choices=[('busy', 'busy'), ('idle', 'idle'), ('contractor', 'contractor'), ('partial', 'partial'), ('N/A', 'N/A')])

class TargetMarignForm(forms.Form):
    target = forms.DecimalField(max_value=100, decimal_places=2, required=True, label='Enter Target Margin')

class MultiEmployeeIndicator(forms.Form):
    number = forms.IntegerField(min_value=1, max_value=10, label='Number of Employees')
        
    
