from django.shortcuts import render
from ..forms import SingleCalculationForm, MultiEmployeeIndicator, ExtraEmployeeForm, TargetMarignForm
from ..models import Employee
from decimal import Decimal
from django.forms import formset_factory
from django.views import View
from .topic import Project


######################################################################################################################################################

def calculator(request):

    selected_employee = None
    target_margin = None
    resulting_margin = None
    comparative_result = None
    weekly_revenue = None
    weekly_cost = None

    number_of_employees = 1
    multiple_employee_form = MultiEmployeeIndicator(request.GET)
    if multiple_employee_form.is_valid():
            number_of_employees = multiple_employee_form.cleaned_data['number']

    target_margin_form = TargetMarignForm(request.POST or None)

    project = Project()

    if number_of_employees == 1: 
        formset = SingleCalculationForm(request.POST or None)
        if request.method == 'POST':
            if formset.is_valid():
                selected_name = formset.cleaned_data['employee']
                selected_employee = Employee.objects.get(name=selected_name)
                employee_dict = {
                    'name': selected_employee.name,
                    'rate': formset.cleaned_data['project_rate']
                }
                project.add_employee(employee_dict)

                if target_margin_form.is_valid():
                    resulting_margin = project.get_resulting_margin(formset.cleaned_data['project_rate'], selected_employee.hourly_rate)
                    if resulting_margin is not None: 
                        resulting_margin *= 100
                    target_margin = target_margin_form.cleaned_data['target']
                    comparative_result = project.is_profitable(target_margin, resulting_margin)

    if number_of_employees > 1: 
        ExtraEmployeeFormSet = formset_factory(ExtraEmployeeForm, extra=number_of_employees)
        formset = ExtraEmployeeFormSet(request.POST or None)
        if request.method == 'POST':
            if formset.is_valid():
                hourly_rates = []
                for form in formset:
                    selected_name = form.cleaned_data['employee']
                    selected_employee = Employee.objects.get(name=selected_name)
                    employee_dict = {
                    'name': selected_employee.name, 
                    'hours': form.cleaned_data['hours'], 
                    'rate': form.cleaned_data['project_rate'], 
                    'extra_time': form.cleaned_data['extra_time']
                    }
                    hourly_rates.append(selected_employee.hourly_rate)
                    project.add_employee(employee_dict)

                cost = []
                for i in hourly_rates: 
                    cost.append(project.get_weekly_cost(project.employee_list, i))
                weekly_cost = sum(cost)
                weekly_revenue = project.get_weekly_revenue(project.employee_list)

                if target_margin_form.is_valid():
                    resulting_margin = project.get_resulting_margin(weekly_revenue, weekly_cost)
                    if resulting_margin is not None:
                        resulting_margin *= 100 # Make comparisons of percentages with whole numbers
                        target_margin = target_margin_form.cleaned_data['target']
                        comparative_result = project.is_profitable(target_margin, resulting_margin)

    context = {
        'project': project,
        'formset': formset,
        'multiple_employee_form': multiple_employee_form,
        'selected_employee': selected_employee,
        'target_margin_form': target_margin_form,
        ##--------------------------------------------
        'resulting_margin': resulting_margin,
        'target_margin': target_margin,
        'comparative_result': comparative_result,
        ##--------------------------------------------
        'weekly_revenue': weekly_revenue,
        'weekly_cost': weekly_cost, 
        'number_of_employees': number_of_employees, 
    }

    return render(request, 'LoadedCost/index.html', context)

######################################################################################################################################################    

