from django.contrib import admin
from .models import  LeaveType, Holiday, Schedule, TrainingType

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # You can add other fields if needed
    list_filter = ('name',)

class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Only show the name and description
    list_filter = ('name',)

admin.site.register(LeaveType)
admin.site.register(Holiday)
admin.site.register(Schedule)
admin.site.register(TrainingType)