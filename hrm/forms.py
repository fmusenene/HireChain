from django import forms
from .models import Employee, Department, Designation,LeaveType, Holiday, LeaveType, Schedule, Overtime, Indicator, GoalType, TrainingType, Trainer

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'company',  'department', 'designation', 'password', 'joining_date','about', 'profile_image', 'date_of_birth']
        exclude = ['id']
        
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


# Holiday Form
class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['title', 'date', 'description', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


# Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'date_of_birth', 'joining_date', 'company', 'designation', 'profile_image', 'phone', 'about', 'department', 'email', 'password']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    # You can customize form field widgets here if needed
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    designation = forms.ModelChoiceField(queryset=Designation.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __str__(self):
        return self.name
    


class EmployeeForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department")
    designation = forms.ModelChoiceField(queryset=Designation.objects.all(), empty_label="Select Designation")

    class Meta:
        model = Employee
        fields = ['name', 'email', 'department', 'designation', 'profile_image']


# Form for LeaveType
class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name is required")
        return name



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'



class OvertimeForm(forms.ModelForm):
    class Meta:
        model = Overtime
        fields = '__all__'

        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.Select(attrs={'class': 'form-select'}),            
        }


# forms.py
from django import forms
from .models import PerformanceIndicator, Designation

class PerformanceIndicatorForm(forms.ModelForm):
    class Meta:
        model = PerformanceIndicator
        fields = [
            'designation', 'customer_experience', 'marketing', 'management', 'administration',
            'presentation_skills', 'quality_of_work', 'efficiency', 'integrity', 'professionalism',
            'team_work', 'critical_thinking', 'conflict_management', 'attendance', 'ability_to_meet_deadline', 'status'
        ]
        
    designation = forms.ModelChoiceField(queryset=Designation.objects.all(), empty_label="Select Designation")
    customer_experience = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    marketing = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    management = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    administration = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    presentation_skills = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    quality_of_work = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    efficiency = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    integrity = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    professionalism = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    team_work = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    critical_thinking = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    conflict_management = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    attendance = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    ability_to_meet_deadline = forms.ChoiceField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')])
    status = forms.ChoiceField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')])
    appraisal_date = forms.DateField()




class GoalTypeForm(forms.ModelForm):
    class Meta:
        model = GoalType
        fields = ['name']  # Only the fields that exist in the GoalType model



# forms.py
class TrainingTypeForm(forms.ModelForm):
    class Meta:
        model = TrainingType
        fields = ['type', 'description', 'status']


# forms.py
class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ["first_name", "last_name", "role", "phone", "email", "description", "status"]



from django import forms
from .models import Training
from .models import Employee  # Import Employee model if needed

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['training_type', 'trainer', 'employees', 'cost', 'start_date', 'end_date', 'description', 'status']
        widgets = {
            'employees': forms.CheckboxSelectMultiple(),
        }



from django import forms
from .models import Promotion, Department, Designation

class PromotionForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department")
    designation_from = forms.ModelChoiceField(queryset=Designation.objects.all(), empty_label="Select Designation From")
    designation_to = forms.ModelChoiceField(queryset=Designation.objects.all(), empty_label="Select Designation To")

    class Meta:
        model = Promotion
        fields = ['employee', 'department', 'designation_from', 'designation_to', 'promotion_date']
        widgets = {
            'promotion_date': forms.DateInput(attrs={'type': 'date'}),
        }



from django import forms
from .models import Resignation

class ResignationForm(forms.ModelForm):
    class Meta:
        model = Resignation
        fields = ['employee', 'notice_date', 'resignation_date', 'reason']
        widgets = {
            'notice_date': forms.DateInput(attrs={'type': 'date'}),
            'resignation_date': forms.DateInput(attrs={'type': 'date'}),
        }


from django import forms
from .models import Termination

class TerminationForm(forms.ModelForm):
    class Meta:
        model = Termination
        fields = ['employee', 'termination_type', 'notice_date', 'reason', 'resignation_date']
        widgets = {
            'notice_date': forms.DateInput(attrs={'type': 'date'}),
            'resignation_date': forms.DateInput(attrs={'type': 'date'}),
        }
