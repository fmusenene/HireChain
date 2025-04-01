from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import EmployeeForm, HolidayForm, LeaveTypeForm, ScheduleForm, OvertimeForm, PerformanceIndicatorForm, GoalTypeForm, TrainingTypeForm
from .models import TrainingType
from django.urls import reverse
from .models import Employee, Designation, Department, Policy, Holiday, LeaveType, Timesheet, Project, Attendance, JobTitle, Overtime, Indicator, GoalType, Leave, Shift
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from datetime import datetime, date, timedelta
import re
import random
import string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import models
from calendar import month_name
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from . import views
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get current date and time
    today = timezone.now().date()
    current_time = timezone.now()
    
    # Get employee statistics
    total_employees = Employee.objects.count()
    present_count = Attendance.objects.filter(attendance_date=today, status='present').count()
    on_leave_count = Leave.objects.filter(from_date__lte=today, to_date__gte=today, status='approved').count()
    
    # Get pending tasks count (placeholder for now)
    pending_tasks_count = 0  # We'll implement this later when we have the Task model
    
    # Get recent activities (placeholder for now)
    recent_activities = []  # We'll implement this later when we have the Activity model
    
    # Get upcoming events (holidays, birthdays, etc.)
    upcoming_events = []
    
    # Add upcoming holidays
    upcoming_holidays = Holiday.objects.filter(date__gte=today).order_by('date')[:3]
    for holiday in upcoming_holidays:
        upcoming_events.append({
            'title': holiday.title,
            'date': holiday.date,
            'type': 'holiday'
        })
    
    # Add upcoming birthdays
    upcoming_birthdays = Employee.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day__gte=today.day
    ).order_by('date_of_birth__day')[:3]
    
    for employee in upcoming_birthdays:
        upcoming_events.append({
            'title': f"{employee.name}'s Birthday",
            'date': employee.date_of_birth.replace(year=today.year),
            'type': 'birthday'
        })
    
    # Sort events by date
    upcoming_events.sort(key=lambda x: x['date'])
    
    context = {
        'today': today,
        'current_time': current_time,
        'total_employees': total_employees,
        'present_count': present_count,
        'on_leave_count': on_leave_count,
        'pending_tasks_count': pending_tasks_count,
        'recent_activities': recent_activities,
        'upcoming_events': upcoming_events[:5],  # Limit to 5 events
    }
    
    return render(request, 'hrm/dashboard.html', context)


def generate_sequential_employee_id():
    """ Generate a unique sequential employee ID (EMP001, EMP002, etc.) """
    last_employee = Employee.objects.order_by('-id').first()

    if last_employee:
        # Extract numeric part using regex
        match = re.match(r"EMP(\d+)", last_employee.employee_id)
        if match:
            last_number = int(match.group(1))  # Extract number
            new_number = last_number + 1
        else:
            new_number = 1  # Reset if the last ID is incorrectly formatted
    else:
        new_number = 1  # Start from EMP001 if no employees exist

    new_employee_id = f"EMP{new_number:03d}"

    # Ensure employee_id is unique
    while Employee.objects.filter(employee_id=new_employee_id).exists():
        new_number += 1
        new_employee_id = f"EMP{new_number:03d}"

    return new_employee_id

def employee_list(request):
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            joining_date = request.POST.get('joining_date', None)
            about = request.POST.get('about', '').strip()
            profile_image = request.FILES.get('profile_image', None)
            date_of_birth = request.POST.get('date_of_birth', None)
            password = request.POST.get('password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()

            # Validate required fields
            if not name or not email or not password or not confirm_password:
                messages.error(request, "Please fill in all required fields!")
                return redirect('employee_list')

            # Validate email uniqueness
            if Employee.objects.filter(email=email).exists():
                messages.error(request, "An employee with this email already exists!")
                return redirect('employee_list')

            # Validate passwords
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect('employee_list')

            if (
                len(password) < 8 or
                not any(char.isupper() for char in password) or
                not any(char.isdigit() for char in password) or
                not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
            ):
                messages.error(request, "Password must be at least 8 characters, include one uppercase letter, one number, and one special character!")
                return redirect('employee_list')

            # Validate and fetch foreign keys
            try:
                designation = Designation.objects.get(id=request.POST['designation'])
                department = Department.objects.get(id=request.POST['department'])
            except (Designation.DoesNotExist, Department.DoesNotExist):
                messages.error(request, "Invalid Designation or Department selected!")
                return redirect('employee_list')

            # Generate sequential employee ID
            employee_id = generate_sequential_employee_id()

            # Create employee object
            employee = Employee.objects.create(
                name=name,
                email=email,
                phone=phone,
                joining_date=joining_date,
                designation=designation,
                department=department,
                password=make_password(password),  # Hash password
                about=about,
                employee_id=employee_id,
                profile_image=profile_image,
                date_of_birth=date_of_birth,
            )

            messages.success(request, f"Employee added successfully with ID: {employee_id}")
            return redirect('employee_list')

        except IntegrityError:
            messages.error(request, "There was an error saving the employee. Please try again.")
            return redirect('employee_list')

        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
            return redirect('employee_list')

    # Retrieve existing employees, designations, and departments
    employees = Employee.objects.all().order_by('-id')
    designations = Designation.objects.all()
    departments = Department.objects.all()

    return render(request, 'hrm/employee_list.html', {
        'designations': designations,
        'departments': departments,
        'employees': employees
    })

@login_required
def edit_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        if request.method == 'POST':
            # Update employee information
            employee.name = request.POST.get('name')
            employee.email = request.POST.get('email')
            employee.phone = request.POST.get('phone')
            employee.department_id = request.POST.get('department')
            employee.designation_id = request.POST.get('designation')
            employee.status = request.POST.get('status')

            # Handle profile image
            if 'profile_image' in request.FILES:
                employee.profile_image = request.FILES['profile_image']

            employee.save()
            messages.success(request, 'Employee information updated successfully.')
            return redirect('employee_list')
        
        # For GET request, return to employee list
        return redirect('employee_list')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('employee_list')

@login_required
def delete_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        if request.method == 'POST':
            # Delete the employee's profile image if it exists
            if employee.profile_image:
                employee.profile_image.delete()
            
            # Delete the employee directly without handling training relationships
            Employee.objects.filter(id=employee_id).delete()
            messages.success(request, 'Employee deleted successfully.')
        else:
            messages.error(request, 'Invalid request method.')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
    
    return redirect('employee_list')

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Calculate years of experience
    if employee.joining_date:
        years_of_experience = (timezone.now().date() - employee.joining_date).days // 365
    else:
        years_of_experience = 0
    
    context = {
        'employee': employee,
        'years_of_experience': years_of_experience,
    }
    
    return render(request, 'hrm/employee_detail.html', context)

def employee_profile(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    emergency_contacts = employee.emergency_contacts.all()
    educations = employee.educations.all()
    experiences = employee.experiences.all()
    projects = employee.projects.all()
    assets = employee.assets.all()
    years_of_experience = date.today().year - employee.joining_date.year

    context = {
        'employee': employee,
        'emergency_contacts': emergency_contacts,
        'educations': educations,
        'experiences': experiences,
        'projects': projects,
        'assets': assets,
        'years_of_experience': years_of_experience
    }
    return render(request, 'hrm/employee_profile.html', context)



def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Error updating employee.')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'hrm/edit_employee.html', {'form': form, 'employee': employee})


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list')

    return render(request, 'hrm/delete_employee.html', {'employee': employee})


def about(request):
    return render(request, 'hrm/about.html')


def departments(request):
    if request.method == 'POST':
        # Fetch form data using the correct field names
        department_name = request.POST.get('department_name')  # Use the form field's name attribute
        status = request.POST.get('status')  # Use the form field's name attribute

        if department_name and status:
            # Save the new department
            Department.objects.create(name=department_name, status=status)
            messages.success(request, f'Department "{department_name}" has been added successfully!')
        else:
            messages.error(request, 'Please fill in all fields before submitting.')

        return redirect('departments')  # Redirect to prevent form resubmission

    # Handle GET request to display all departments
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'hrm/departments.html', context)


def designations(request):
    if request.method == 'POST':
        # Fetch form data
        designation_name = request.POST.get('designation_name')
        department = request.POST.get('department_name')  # This will be the department id
        status = request.POST.get('status')

        if designation_name and department and status:
            try:
                # Fetch the Department object using the department ID
                department = Department.objects.get(id=department)
                
                # Create and save the new Designation
                Designation.objects.create(name=designation_name, department=department, status=status)
                messages.success(request, f'Designation "{designation_name}" has been added successfully!')
                return redirect('designations')  # Redirect to the same page to prevent form resubmission
            except Department.DoesNotExist:
                messages.error(request, f'Department with ID {department} does not exist.')
            except Exception as e:
                messages.error(request, f'Error adding designation: {e}')
        else:
            messages.error(request, 'Please fill in all fields before submitting.')

    # Fetch all existing designations to display them
    designations = Designation.objects.all()

    # Fetch departments to populate the department dropdown in the form
    departments = Department.objects.all()

    # Render the template with designations and departments
    return render(request, 'hrm/designations.html', {
        'designations': designations,
        'departments': departments
    })
    
# policies views
def policies(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        # Fetching form data
        policy_name = request.POST.get('policy_name')
        department_id = request.POST.get('department_id')  # Fix: use department_id
        appraisal_date = request.POST.get('appraisal_date')
        description = request.POST.get('description')
        policy_file = request.FILES.get('policy_file')

        # Validate appraisal_date
        try:
            if appraisal_date:
                appraisal_date = datetime.strptime(appraisal_date, '%Y-%m-%d').date()
            else:
                raise ValueError("Appraisal date is required.")
        except ValueError as e:
            messages.error(request, f"Invalid appraisal date: {e}")
            return redirect('policies')

        # Validate other fields
        if policy_name and department_id and appraisal_date and description:
            try:
                # Fetch the department object
                department = Department.objects.get(id=department_id)
                # Create and save the new policy
                policy = Policy(
                    name=policy_name,
                    department=department,
                    description=description,
                    appraisal_date=appraisal_date,
                    policy_file=policy_file
                )
                policy.save()

                # Success message
                messages.success(request, f'Policy "{policy_name}" has been added successfully!')
                return redirect('policies')
            except Exception as e:
                messages.error(request, f'Error adding policy: {e}')
                return redirect('policies')
        else:
            messages.error(request, 'Please fill in all fields before submitting.')
            return redirect('policies')

    # If it's a GET request, we fetch all policies and departments to display them
    policies = Policy.objects.all()
    context = {
        'policys': policies,
        'departments': departments,
    }

    return render(request, 'hrm/policies.html', context)

# birthdays views
def birthdays(request):
    today = date.today()
    employees = Employee.objects.all()  # Fetch all employees
    departments = Department.objects.all()  # Fetch all departments

    # Define months for the dropdown
    months = [{"value": f"{i:02}", "name": month_name[i]} for i in range(1, 13)]

    # Get filter values from the GET parameters
    month = request.GET.get('month')
    department = request.GET.get('department')

    # Apply filters if provided
    if month:
        employees = employees.filter(date_of_birth__month=month)
    if department:
        employees = employees.filter(department__name=department)

    # Calculate days remaining for all employees
    birthdays = []
    for emp in employees:
        if emp.date_of_birth:  # Ensure date_of_birth is not null
            next_birthday = emp.date_of_birth.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_remaining = (next_birthday - today).days
            birthdays.append({
                "profile_image": emp.profile_image.url if emp.profile_image else "/media/profile_images/default_profile.png",
                "name": emp.name,
                "department": emp.department.name if emp.department else "N/A",
                "designation": emp.designation.name if emp.designation else "N/A",
                "date_of_birth": emp.date_of_birth,
                "days_remaining": days_remaining,
            })

    # Sort the list by days remaining
    birthdays = sorted(birthdays, key=lambda x: x["days_remaining"])

    context = {
        "birthdays": birthdays,
        "departments": departments,
        "months": months,
    }

    return render(request, "hrm/birthdays.html", context)


def holidays(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()  # Save the holiday to the database
            messages.success(request, 'Holiday has been added successfully.')
            return redirect('holidays')  # Redirect back to the holidays list view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:

        form = HolidayForm()

    holidays = Holiday.objects.all()  # Fetch all holidays
    return render(request, 'hrm/holidays.html', {'form': form, 'holidays': holidays})


def leave_type(request, id=None):
    if request.method == 'POST':
        if 'delete' in request.path:
            try:
                leave_type = LeaveType.objects.get(id=id)
                leave_type.delete()
                messages.success(request, 'Leave type deleted successfully.')
                return JsonResponse({'status': 'success'})
            except LeaveType.DoesNotExist:
                messages.error(request, 'Leave type not found.')
                return JsonResponse({'status': 'error', 'message': 'Leave type not found'}, status=404)
            except Exception as e:
                messages.error(request, f'Error deleting leave type: {str(e)}')
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        action = request.POST.get('action')
        if action == 'edit':
            try:
                leave_type = LeaveType.objects.get(id=id)
                leave_type.name = request.POST.get('name')
                leave_type.description = request.POST.get('description')
                leave_type.days_allowed = request.POST.get('days_allowed')
                leave_type.save()
                messages.success(request, 'Leave type updated successfully.')
            except LeaveType.DoesNotExist:
                messages.error(request, 'Leave type not found.')
            except Exception as e:
                messages.error(request, f'Error updating leave type: {str(e)}')
        else:
            form = LeaveTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Leave type added successfully.')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        return redirect('leave_type')

    form = LeaveTypeForm()
    leave_types = LeaveType.objects.all()
    context = {
        'form': form,
        'leave_types': leave_types
    }
    return render(request, 'hrm/leave_type.html', context)

# timesheet view function
def timesheets(request):
    # Get filter parameters
    project_id = request.GET.get('project')
    sort_by = request.GET.get('sort_by', 'last_7_days')
    search_query = request.GET.get('search', '')
    rows_per_page = int(request.GET.get('rows_per_page', 10))

    # Base queryset with related fields
    queryset = Timesheet.objects.select_related(
        'employee',
        'project'
    ).order_by('-date')

    # Apply project filter
    if project_id:
        queryset = queryset.filter(project_id=project_id)

    # Apply date filter
    today = timezone.now().date()
    if sort_by == 'last_7_days':
        queryset = queryset.filter(date__gte=today - timezone.timedelta(days=7))
    elif sort_by == 'last_30_days':
        queryset = queryset.filter(date__gte=today - timezone.timedelta(days=30))
    elif sort_by == 'last_90_days':
        queryset = queryset.filter(date__gte=today - timezone.timedelta(days=90))

    # Apply search filter
    if search_query:
        queryset = queryset.filter(
            models.Q(employee__name__icontains=search_query) |
            models.Q(project__name__icontains=search_query)
        )

    # Get all projects for the dropdown
    projects = Project.objects.all()

    context = {
        'timesheets': queryset,
        'projects': projects,
        'current_project': project_id,
        'current_sort': sort_by,
        'search_query': search_query,
        'rows_per_page': rows_per_page,
        'sort_options': [
            ('last_7_days', 'Last 7 Days'),
            ('last_30_days', 'Last 30 Days'),
            ('last_90_days', 'Last 90 Days'),
        ]
    }

    return render(request, 'hrm/timesheets.html', context)




# attendance admin view
@login_required
def admin_attendance(request):
    if request.method == 'POST':
        attendance_id = request.POST.get('attendance_id')
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            attendance.attendance_date = request.POST.get('attendance_date')
            attendance.check_in = request.POST.get('check_in')
            attendance.check_out = request.POST.get('check_out')
            attendance.break_time = request.POST.get('break_time')
            attendance.late_minutes = request.POST.get('late_minutes', 0)
            attendance.production_hours = request.POST.get('production_hours')
            attendance.status = request.POST.get('status', 'present')
            attendance.save()
            messages.success(request, 'Attendance updated successfully')
        except Attendance.DoesNotExist:
            messages.error(request, 'Attendance record not found')
        except Exception as e:
            messages.error(request, f'Error updating attendance: {str(e)}')
        return redirect('admin_attendance')

    today = timezone.now().date()
    employees = Employee.objects.select_related('department').all()
    
    try:
        attendances = Attendance.objects.filter(attendance_date=today).select_related('employee')
        total_employees = employees.count()
        present_count = attendances.filter(status='present').count()
        late_count = attendances.filter(status='late').count()
        uninformed_count = attendances.filter(status='uninformed').count()
        permission_count = attendances.filter(status='permission').count()
        absent_count = total_employees - (present_count + late_count + uninformed_count + permission_count)
    except Exception as e:
        attendances = []
        total_employees = employees.count()
        present_count = late_count = uninformed_count = permission_count = 0
        absent_count = total_employees

    context = {
        'employees': employees,
        'attendances': attendances,
        'total_employees': total_employees,
        'present_count': present_count,
        'late_count': late_count,
        'uninformed_count': uninformed_count,
        'permission_count': permission_count,
        'absent_count': absent_count,
        'today': today,
    }
    return render(request, 'hrm/admin_attendance.html', context)



@login_required
def employee_attendance(request):
    # First try to get employee by email
    employee = Employee.objects.filter(email=request.user.email).first()
    
    # If not found by email, try to get by user relationship
    if not employee:
        employee = Employee.objects.filter(user=request.user).first()
        
    # If still no employee found, create a new employee record
    if not employee:
        try:
            # Get or create default department
            default_department, _ = Department.objects.get_or_create(
                name="General",
                defaults={'status': 'active'}
            )
            
            # Get or create default designation
            default_designation, _ = Designation.objects.get_or_create(
                name="Employee",
                defaults={
                    'department': default_department,
                    'status': 'active'
                }
            )
            
            # Generate employee ID
            last_employee = Employee.objects.order_by('-id').first()
            new_number = 1
            if last_employee:
                try:
                    last_id = int(last_employee.employee_id.replace('EMP', ''))
                    new_number = last_id + 1
                except (ValueError, AttributeError):
                    pass
            
            employee_id = f"EMP{new_number:03d}"
            
            # Create the employee
            employee = Employee.objects.create(
                user=request.user,
                email=request.user.email,
                name=request.user.get_full_name() or request.user.username,
                employee_id=employee_id,
                joining_date=timezone.now().date(),
                department=default_department,
                designation=default_designation
            )
            messages.success(request, 'Employee profile created successfully.')
        except Exception as e:
            messages.error(request, f'Could not create employee profile: {str(e)}')
            return render(request, 'hrm/employee_attendance.html', {'error': str(e)})
        
    now = timezone.now()
    today = now.date()

    # Get today's attendance
    try:
        today_attendance = Attendance.objects.get(
            employee=employee,
            attendance_date=today
        )
    except Attendance.DoesNotExist:
        today_attendance = None

    # Calculate statistics
    current_week_start = today - timezone.timedelta(days=today.weekday())
    current_month_start = today.replace(day=1)

    # Weekly hours
    week_attendances = Attendance.objects.filter(
        employee=employee,
        attendance_date__gte=current_week_start,
        attendance_date__lte=today
    )
    total_week_hours = sum([attendance.get_production_hours() for attendance in week_attendances], timezone.timedelta())
    total_week_target = timezone.timedelta(hours=40)  # 40 hours per week
    week_percentage = (total_week_hours.total_seconds() / total_week_target.total_seconds()) * 100 if total_week_target.total_seconds() > 0 else 0

    # Monthly hours
    month_attendances = Attendance.objects.filter(
        employee=employee,
        attendance_date__gte=current_month_start,
        attendance_date__lte=today
    )
    total_month_hours = sum([attendance.get_production_hours() for attendance in month_attendances], timezone.timedelta())
    total_month_target = timezone.timedelta(hours=98)  # Approximately 98 hours per month
    month_percentage = (total_month_hours.total_seconds() / total_month_target.total_seconds()) * 100 if total_month_target.total_seconds() > 0 else 0

    # Overtime this month
    total_overtime = sum([attendance.get_overtime_hours() for attendance in month_attendances], timezone.timedelta())
    overtime_target = timezone.timedelta(hours=28)  # 28 hours overtime target
    overtime_percentage = (total_overtime.total_seconds() / overtime_target.total_seconds()) * 100 if overtime_target.total_seconds() > 0 else 0

    # Today's statistics
    if today_attendance:
        total_hours_today = today_attendance.get_production_hours()
        productive_hours = today_attendance.get_productive_hours()
        break_hours = today_attendance.get_break_hours()
        overtime_hours = today_attendance.get_overtime_hours()
    else:
        total_hours_today = timezone.timedelta()
        productive_hours = timezone.timedelta()
        break_hours = timezone.timedelta()
        overtime_hours = timezone.timedelta()

    context = {
        'employee': employee,
        'today': today,
        'current_time': now,
        'today_attendance': today_attendance,
        'total_hours_today': total_hours_today,
        'total_week_hours': total_week_hours,
        'week_percentage': week_percentage,
        'total_month_hours': total_month_hours,
        'month_percentage': month_percentage,
        'total_overtime': total_overtime,
        'overtime_percentage': overtime_percentage,
        'productive_hours': productive_hours,
        'break_hours': break_hours,
        'overtime_hours': overtime_hours,
    }
    
    return render(request, 'hrm/employee_attendance.html', context)



def employee_availability(request):
    # Get search query and pagination parameters
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    entries_per_page = request.GET.get('entries', 10)
    sort_by = request.GET.get('sort_by', '7')  # Default to 7 days
    
    # Calculate date range based on sort selection
    today = timezone.now().date()
    if sort_by == '30':
        start_date = today - timedelta(days=30)
    elif sort_by == '90':
        start_date = today - timedelta(days=90)
    else:  # Default to 7 days
        start_date = today - timedelta(days=7)
    
    # Base queryset
    employees = Employee.objects.all()
    
    # Apply search filter if search query exists
    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(designation__name__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )
    
    # Get departments for the form
    departments = Department.objects.all()
    
    # Setup pagination
    paginator = Paginator(employees, int(entries_per_page))
    page_obj = paginator.get_page(page_number)
    
    # Calculate date range for display
    end_date = today
    date_range = f"{start_date.strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')}"
    
    context = {
        'employees': page_obj,
        'departments': departments,
        'search_query': search_query,
        'date_range': date_range,
        'sort_by': sort_by,
        'entries_per_page': entries_per_page,
        'total_entries': employees.count(),
        'page_range': range(1, paginator.num_pages + 1),
    }
    return render(request, 'hrm/employee_availability.html', context)

def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            return redirect('employee_availability')
    else:
        form = ScheduleForm()
        departments = Department.objects.all()
        job_titles = JobTitle.objects.all()
        return render(request, 'hrm/add_schedule_modal.html', {'form': form, 'departments': departments, 'job_titles': job_titles})

class JobTitleview(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ScheduleView(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    shift = models.CharField(max_length=50)  # e.g., "Morning", "Afternoon", "Night"
    min_start_time = models.TimeField()
    start_time = models.TimeField()
    max_start_time = models.TimeField()
    min_end_time = models.TimeField()
    end_time = models.TimeField()
    max_end_time = models.TimeField()
    break_time = models.CharField(max_length=50)  # e.g., "30 minutes"
    accept_extra_hours = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    # ... other schedule fields

    def __str__(self):
        return f"{self.employee.name} - {self.date}"



def overtime_records(request):
    overtimes = Overtime.objects.all()
    form = OvertimeForm()
    return render(request, 'hrm/overtime.html', {'overtimes': overtimes, 'form': form})

def overtime(request):
    if request.method == 'POST':
        form = OvertimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('overtime_records')  # Redirect to the records page
    else:
        form = OvertimeForm()
    
    return render(request, 'hrm/overtime.html', {'form': form})


def performance_indicator(request):
    if request.method == 'POST':
        form = PerformanceIndicatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance_indicator')  # Redirect to avoid re-submitting the form on refresh
    else:
        form = PerformanceIndicatorForm()

    return render(request, 'hrm/performance_indicator.html', {'form': form})



from django.shortcuts import render, redirect
from .models import Employee, PerformanceIndicator  # Ensure these models exist
from django.http import JsonResponse

def performance_appraisal(request):
    employees = Employee.objects.all()  # Fetch employees with related fields

    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        appraisal_date = request.POST.get("appraisal_date")
        status = request.POST.get("status")

        # Ensure Employee exists
        employee = Employee.objects.get(id=employee_id)

        # Save Appraisal Record
        PerformanceIndicator.objects.create(
            employee=employee,
            appraisal_date=appraisal_date,
            status=status
        )
        return JsonResponse({"message": "Appraisal added successfully!"}, status=201)

    return render(request, "hrm/Performance_Appraisal.html", {"employees": employees})



class GoalTypeView(TemplateView):
    template_name = 'hrm/goal_types.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goals'] = GoalType.objects.all()  # Pass all goal types
        context['form'] = GoalTypeForm()  # Pass empty form for the modal
        return context

    def post(self, request, *args, **kwargs):
        form = GoalTypeForm(request.POST)  # Get form data
        if form.is_valid():  # Check if form is valid
            form.save()  # Save the goal type to the database
            return HttpResponseRedirect(reverse('goal_type_view'))  # Redirect to refresh page with the new goal
        # If form is not valid, render the page again with the form errors
        return self.render_to_response({'form': form})

from django.shortcuts import render
from django.views.generic import View

class GoalTrackingView(View):
    def get(self, request, *args, **kwargs):
        # Your logic for the view
        return render(request, 'hrm/goal_types.html')



class TrainingTypeView(View):
    def get(self, request):
        Training_Types = TrainingType.objects.all()
        form = TrainingTypeForm()
        return render(request, 'hrm/Training_Type.html', {'training_types': Training_Types, 'form': form})

    def post(self, request):
        
        form = TrainingTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_type')  
        
        # Debugging: Print errors
        print("Form errors:", form.errors)
        
        return render(request, 'hrm/Training_Type.html', {'form': form, 'Training_Types': TrainingType.objects.all()})
    

    # views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import Trainer
from .forms import TrainerForm

class TrainerListView(ListView):
    model = Trainer
    template_name = "hrm/trainers.html"
    context_object_name = "trainers"

    # Override get_context_data to include the form and the list of trainers
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TrainerForm()  # Include the form for creating a new trainer
        context['form_submitted'] = False  # Add a flag to indicate form submission status
        return context

    # Handle form submission in a POST method
    def post(self, request, *args, **kwargs):
        form = TrainerForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new trainer
            return redirect(reverse_lazy("trainers"))  # Redirect to the same page after adding
        trainers = Trainer.objects.all()
        context = self.get_context_data(form=form, trainers=trainers, form_submitted=True)
        return self.render_to_response(context)




from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Training, TrainingType, Trainer, Employee
from .forms import TrainingForm

class TrainingListView(View):
    def get(self, request):
        # Get all the relevant data
        trainings = Training.objects.all()
        training_types = TrainingType.objects.all()
        trainers = Trainer.objects.all()
        employees = Employee.objects.all()
        form = TrainingForm()

        context = {
            'trainings': trainings,
            'form': form,
            'training_types': training_types,
            'trainers': trainers,
            'employees': employees,
        }

        return render(request, 'hrm/training_list.html', context)

    def post(self, request):
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_list')
        else:
            # If form is not valid, render the page with the error messages
            return self.get(request)



from django.shortcuts import render, redirect
from django.views import View
from .models import Promotion, Department, Designation, Employee
from .forms import PromotionForm

class PromotionListView(View):
    def get(self, request):
        promotions = Promotion.objects.all()
        departments = Department.objects.all()
        designations = Designation.objects.all()
        employees = Employee.objects.all()
        form = PromotionForm()
        return render(request, 'hrm/promotion.html', {
            'promotions': promotions,
            'departments': departments,
            'designations': designations,
            'employees': employees,
            'form': form
        })

    def post(self, request):
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promotion_list')
        else:
            promotions = Promotion.objects.all()
            departments = Department.objects.all()
            designations = Designation.objects.all()
            employees = Employee.objects.all()
            return render(request, 'hrm/promotion.html', {
                'promotions': promotions,
                'departments': departments,
                'designations': designations,
                'employees': employees,
                'form': form
            })



from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from .models import Resignation, Employee
from .forms import ResignationForm

class ResignationView(FormMixin, ListView):
    model = Resignation
    template_name = "hrm/resignation.html"
    context_object_name = "resignations"
    form_class = ResignationForm
    success_url = reverse_lazy("resignation_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["employees"] = Employee.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.shortcuts import render
from .models import Termination, Employee
from .forms import TerminationForm

class TerminationListView(CreateView, ListView):
    model = Termination
    template_name = "hrm/termination.html"
    form_class = TerminationForm
    success_url = reverse_lazy('termination_list')  # Ensure this matches your URL name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terminations'] = Termination.objects.all()
        context['employees'] = Employee.objects.all()
        return context

def leave_management(request):
    if request.method == 'POST':
        # Handle leave creation
        employee_id = request.POST.get('employee')
        leave_type_id = request.POST.get('leave_type')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        no_of_days = request.POST.get('no_of_days')
        remaining_days = request.POST.get('remaining_days')
        reason = request.POST.get('reason')

        # Debug print
        print("Received form data:", {
            'employee_id': employee_id,
            'leave_type_id': leave_type_id,
            'from_date': from_date,
            'to_date': to_date,
            'no_of_days': no_of_days,
            'remaining_days': remaining_days,
            'reason': reason
        })

        try:
            # Validate required fields
            if not all([employee_id, leave_type_id, from_date, to_date, no_of_days, reason]):
                missing_fields = []
                if not employee_id: missing_fields.append('Employee')
                if not leave_type_id: missing_fields.append('Leave Type')
                if not from_date: missing_fields.append('From Date')
                if not to_date: missing_fields.append('To Date')
                if not no_of_days: missing_fields.append('Number of Days')
                if not reason: missing_fields.append('Reason')
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Get employee and leave type
            try:
                employee = Employee.objects.get(id=employee_id)
            except Employee.DoesNotExist:
                raise ValueError(f"Employee with ID {employee_id} does not exist.")

            try:
                leave_type = LeaveType.objects.get(id=leave_type_id)
            except LeaveType.DoesNotExist:
                raise ValueError(f"Leave type with ID {leave_type_id} does not exist.")
            
            # Convert and validate dates
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD format.")

            # Validate date range
            if from_date > to_date:
                raise ValueError("End date cannot be earlier than start date.")

            # Validate number of days
            try:
                no_of_days = int(no_of_days)
                remaining_days = int(remaining_days)
                if no_of_days <= 0:
                    raise ValueError("Number of days must be greater than 0.")
            except ValueError:
                raise ValueError("Invalid number of days format.")
            
            # Debug print
            print("Creating leave with:", {
                'employee': employee.id,
                'leave_type': leave_type.id,
                'from_date': from_date,
                'to_date': to_date,
                'no_of_days': no_of_days,
                'remaining_days': remaining_days,
                'reason': reason
            })
            
            # Create leave record
            leave = Leave.objects.create(
                employee=employee,
                leave_type=leave_type,
                from_date=from_date,
                to_date=to_date,
                no_of_days=no_of_days,
                remaining_days=remaining_days,
                reason=reason,
                status='pending'
            )
            
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('leave_admin')
            
        except ValueError as e:
            messages.error(request, f'Error submitting leave request: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error submitting leave request: {str(e)}')
            print("Exception details:", str(e))  # Debug print

    # For GET requests, display the leave management page
    leaves = Leave.objects.select_related('employee', 'leave_type').all().order_by('-created_at')
    employees = Employee.objects.all()
    leave_types = LeaveType.objects.all()
    
    context = {
        'leaves': leaves,
        'employees': employees,
        'leave_types': leave_types,
    }
    
    return render(request, 'hrm/leave_admin.html', context)

def edit_department(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        if request.method == 'POST':
            department.name = request.POST.get('department_name')
            department.status = request.POST.get('status')
            department.save()
            messages.success(request, f'Department "{department.name}" has been updated successfully!')
            return redirect('departments')
    except Department.DoesNotExist:
        messages.error(request, 'Department not found.')
        return redirect('departments')

def delete_department(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        if request.method == 'POST':
            # Check for related objects
            related_objects = []
            
            # Check for employees
            if department.employee_set.exists():
                related_objects.append("employees")
            
            # Check for designations
            if department.designation_set.exists():
                related_objects.append("designations")
            
            # Check for policies
            if department.policy_set.exists():
                related_objects.append("policies")
            
            # Check for schedules
            if department.schedule_set.exists():
                related_objects.append("schedules")
            
            # If there are related objects, show error message
            if related_objects:
                messages.error(request, f'Cannot delete department "{department.name}" because it has related {", ".join(related_objects)}. Please delete or reassign these items first.')
                return redirect('departments')
            
            # If no related objects, proceed with deletion
            department_name = department.name
            department.delete()
            messages.success(request, f'Department "{department_name}" has been deleted successfully!')
        else:
            messages.error(request, 'Invalid request method.')
    except Department.DoesNotExist:
        messages.error(request, 'Department not found.')
    
    return redirect('departments')

@login_required
def leave_employee(request):
    # Try to get the employee profile by email first
    try:
        employee = Employee.objects.get(email=request.user.email)
    except Employee.DoesNotExist:
        # If no employee exists with this email, try to get by user relationship
        try:
            employee = request.user.employee
        except Employee.DoesNotExist:
            messages.error(request, 'No employee profile found. Please contact your administrator.')
            return redirect('hrm')  # Redirect to home page with error message

    if request.method == 'POST':
        # Handle leave request submission
        leave_type_id = request.POST.get('leave_type')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        no_of_days = request.POST.get('no_of_days')
        reason = request.POST.get('reason')

        try:
            leave_type = LeaveType.objects.get(id=leave_type_id)
            
            leave = Leave.objects.create(
                employee=employee,
                leave_type=leave_type,
                from_date=from_date,
                to_date=to_date,
                no_of_days=no_of_days,
                remaining_days=leave_type.days_allowed - int(no_of_days),  # Using days_allowed instead of default_days
                reason=reason,
                status='pending'
            )
            messages.success(request, 'Leave request submitted successfully.')
        except Exception as e:
            messages.error(request, f'Error submitting leave request: {str(e)}')
        
        return redirect('leave_employee')

    # Calculate leave statistics for each leave type
    leave_stats = {}
    leave_types = LeaveType.objects.all()
    
    for leave_type in leave_types:
        # Get all approved leaves for this type
        approved_leaves = Leave.objects.filter(
            employee=employee,
            leave_type=leave_type,
            status='approved'
        )
        
        # Calculate total days taken
        total_days_taken = sum(leave.no_of_days for leave in approved_leaves)
        
        # Calculate remaining days
        remaining_days = max(0, leave_type.days_allowed - total_days_taken)  # Using days_allowed instead of default_days
        
        leave_stats[leave_type.name.lower()] = {
            'total': total_days_taken,
            'remaining': remaining_days
        }

    # Get all leaves for this employee
    leaves = Leave.objects.filter(employee=employee).order_by('-created_at')
    
    context = {
        'leaves': leaves,
        'leave_types': leave_types,
        'leave_stats': leave_stats,
        'annual_leaves': leave_stats.get('annual', {'total': 0, 'remaining': 0}),
        'medical_leaves': leave_stats.get('medical', {'total': 0, 'remaining': 0}),
        'casual_leaves': leave_stats.get('casual', {'total': 0, 'remaining': 0}),
        'other_leaves': leave_stats.get('other', {'total': 0, 'remaining': 0}),
    }
    
    return render(request, 'hrm/leave_employee.html', context)

def employee_details(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    context = {
        'employee': employee,
    }
    return render(request, 'hrm/employee_details.html', context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get current user's employee record
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None
    
    # Get today's date
    today = timezone.now().date()
    
    # Get attendance statistics
    total_employees = Employee.objects.count()
    present_employees = Attendance.objects.filter(date=today, status='present').count()
    total_leaves = Leave.objects.filter(from_date__lte=today, to_date__gte=today, status='approved').count()
    
    # Get pending tasks (assuming you have a Task model)
    pending_tasks = Task.objects.filter(assigned_to=employee, status='pending').count() if employee else 0
    
    # Get recent activities
    recent_activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:5]
    
    context = {
        'employee': employee,
        'total_employees': total_employees,
        'present_employees': present_employees,
        'total_leaves': total_leaves,
        'pending_tasks': pending_tasks,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'dashboard.html', context)
