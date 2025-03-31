from django.db import models
from django.utils import timezone
from django.db.models import Max
import uuid
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django import forms

# Department Model
class Department(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


# Designation Model
class Designation(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'


# Team Model
class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# JobTitle Model
class JobTitle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Employee Model    
class Employee(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    # Personal Information
    employee_id = models.CharField(max_length=10, unique=True, blank=True)
    profile_image = models.ImageField(upload_to='employee_profiles/', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=10, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    confirm_password = models.CharField(max_length=100, null=True, blank=True)  
    company = models.CharField(max_length=100)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    joining_date = models.DateField(default=date.today)
    client_id = models.CharField(max_length=10, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    report_office = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    about = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    passport_expiry_date = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=20, null=True, blank=True)
    employment_of_spouse = models.CharField(max_length=100, null=True, blank=True)
    no_of_children = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            max_id = Employee.objects.all().aggregate(Max('id'))['id__max']
            next_id = 1 if max_id is None else max_id + 1
            self.employee_id = f'EMP{next_id:03d}'
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def days_remaining(self):
        today = timezone.now().date()
        next_birthday = self.date_of_birth.replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    class Meta:
        ordering = ['-joining_date']
        verbose_name = 'Employee'

class EmergencyContact(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.relationship})"

class Education(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=100)
    award = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.school} - {self.award}"

class Experience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return f"{self.company} - {self.role}"

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='project_assignments', null=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.name


# Policy Model
class Policy(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    appraisal_date = models.DateField()
    policy_file = models.FileField(upload_to="policies/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Holiday Model
class Holiday(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'


class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    default_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Leave(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    no_of_days = models.IntegerField(default=0)
    remaining_days = models.IntegerField(default=0)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type.name} ({self.from_date} to {self.to_date})"

    class Meta:
        ordering = ['-created_at']


class Timesheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.name} - {self.project.name} - {self.date}"

    @property
    def remaining_hours(self):
        """Calculate remaining hours dynamically"""
        return self.total_hours - self.worked_hours if self.total_hours and self.worked_hours else 0

    @property
    def completion_percentage(self):
        """Calculate completion percentage"""
        if self.total_hours and self.worked_hours:
            return (self.worked_hours / self.total_hours) * 100
        return 0

class OldAttendance(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    break_time = models.CharField(max_length=20, null=True, blank=True)
    late_minutes = models.IntegerField(default=0)
    production_hours = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('permission', 'Permission'),
        ('uninformed', 'Uninformed')
    ], default='present')

    def __str__(self):
        return f"{self.employee.name} - Old Attendance"

class Attendance(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    attendance_date = models.DateField(default=date.today)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    break_time = models.CharField(max_length=20, null=True, blank=True)
    late_minutes = models.IntegerField(default=0)
    production_hours = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('permission', 'Permission'),
        ('uninformed', 'Uninformed')
    ], default='present')

    def __str__(self):
        return f"{self.employee.name} - {self.attendance_date}"

    def get_production_hours(self):
        if self.check_in and self.check_out:
            check_in_dt = datetime.combine(self.attendance_date, self.check_in)
            check_out_dt = datetime.combine(self.attendance_date, self.check_out)
            return check_out_dt - check_in_dt
        return timedelta()

    def get_productive_hours(self):
        total = self.get_production_hours()
        if self.break_time:
            try:
                hours, minutes = map(int, self.break_time.split('h ')[0].split(':'))
                break_delta = timedelta(hours=hours, minutes=minutes)
                return total - break_delta
            except:
                pass
        return total

    def get_break_hours(self):
        if self.break_time:
            try:
                hours, minutes = map(int, self.break_time.split('h ')[0].split(':'))
                return timedelta(hours=hours, minutes=minutes)
            except:
                pass
        return timedelta()

    def get_overtime_hours(self):
        productive_hours = self.get_productive_hours()
        standard_hours = timedelta(hours=8)  # 8 hours standard workday
        if productive_hours > standard_hours:
            return productive_hours - standard_hours
        return timedelta()

    class Meta:
        ordering = ['-attendance_date']

class Schedule(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    shift = models.CharField(max_length=10, choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening')])
    min_start_time = models.TimeField(null=True, blank=True)
    max_end_time = models.TimeField(null=True, blank=True)
    min_end_time = models.TimeField(null=True, blank=True)
    max_start_time = models.TimeField(null=True, blank=True)
    break_time = models.DurationField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_accept_extra_hours = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.username} - {self.day_of_week}"
    

class Overtime(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    remaining_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(
        max_length=10, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.date}"


# models.py
class Indicator(models.Model):
    designation = models.ForeignKey('Designation', on_delete=models.CASCADE)
    customer_experience = models.CharField(max_length=100)
    marketing = models.CharField(max_length=100)
    management = models.CharField(max_length=100)
    administration = models.CharField(max_length=100)
    presentation_skills = models.CharField(max_length=100)
    quality_of_work = models.CharField(max_length=100)
    efficiency = models.CharField(max_length=100)
    integrity = models.CharField(max_length=100)
    professionalism = models.CharField(max_length=100)
    team_work = models.CharField(max_length=100)
    critical_thinking = models.CharField(max_length=100)
    conflict_management = models.CharField(max_length=100)
    attendance = models.CharField(max_length=100)
    ability_to_meet_deadline = models.CharField(max_length=100)
    criteria = models.CharField(max_length=100)
    score = models.IntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=100)
    appraisal_date = models.DateField()

    def __str__(self):
        return f"Performance Indicator for {self.designation}"



class PerformanceIndicator(models.Model):
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    customer_experience = models.CharField(max_length=20)
    marketing = models.CharField(max_length=20)
    management = models.CharField(max_length=20)
    administration = models.CharField(max_length=20)
    presentation_skills = models.CharField(max_length=20)
    quality_of_work = models.CharField(max_length=20)
    efficiency = models.CharField(max_length=20)
    integrity = models.CharField(max_length=20)
    professionalism = models.CharField(max_length=20)
    team_work = models.CharField(max_length=20)
    critical_thinking = models.CharField(max_length=20)
    conflict_management = models.CharField(max_length=20)
    attendance = models.CharField(max_length=20)
    ability_to_meet_deadline = models.CharField(max_length=20)
    criteria = models.CharField(max_length=20)
    score = models.IntegerField()
    status = models.CharField(max_length=20)
    appraisal_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Performance Indicator for {self.designation.name}"
    


class GoalType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# models.py
from django.db import models

class TrainingType(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    def __str__(self):
        return self.type


# models.py
from django.db import models

class Trainer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[("Active", "Active"), ("Inactive", "Inactive")])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


from django.db import models

class Training(models.Model):
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employee)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return f"{self.training_type} - {self.trainer}"


from django.db import models

class Promotion(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    designation_from = models.CharField(max_length=255)
    designation_to = models.CharField(max_length=255)
    promotion_date = models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.promotion_date}"



class Resignation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    notice_date = models.DateField()
    resignation_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.employee.name} - {self.resignation_date}"
    

class Termination(models.Model):
    TERMINATION_TYPES = [
        ('voluntary', 'Voluntary'),
        ('involuntary', 'Involuntary'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    termination_type = models.CharField(max_length=20, choices=TERMINATION_TYPES)
    notice_date = models.DateField()
    reason = models.TextField()
    resignation_date = models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.termination_type}"

class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_time = models.IntegerField(help_text="Break time in minutes")
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name