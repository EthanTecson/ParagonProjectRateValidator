from django.contrib import admin
from .models import Employee

# admin.site.register(Employee)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hourly_rate')

admin.site.register(Employee, EmployeeAdmin)