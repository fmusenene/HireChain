from django import template
from hrm.models import Attendance

register = template.Library()

@register.filter
def get_item(attendances, employee_id):
    """
    Template filter to get an attendance record for a specific employee from a list of attendances
    """
    try:
        # Filter the list to find the attendance record for the employee
        matching_attendances = [a for a in attendances if str(a.employee_id) == str(employee_id)]
        return matching_attendances[0] if matching_attendances else None
    except (AttributeError, IndexError):
        return None 

@register.filter
def percentage(value, total):
    try:
        return (value / total) * 100
    except (ValueError, ZeroDivisionError):
        return 0 