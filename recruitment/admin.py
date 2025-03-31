from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'position_applied', 'status', 'applied_on')
    list_filter = ('status', 'applied_on')
    search_fields = ('full_name', 'email', 'position_applied')
    date_hierarchy = 'applied_on'
    ordering = ('-applied_on',)
    