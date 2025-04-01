from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'profile_image', 'title', 'description', 'category', 'job_type',
            'job_level', 'experience', 'qualification', 'gender',
            'min_salary', 'max_salary', 'address', 'country', 'city',
            'contact', 'location', 'required_skills', 'expired_date'
        ]
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter job description'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Job.CATEGORY_CHOICES),
            'job_type': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Job.JOB_TYPE_CHOICES),
            'job_level': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Job.JOB_LEVEL_CHOICES),
            'experience': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Job.EXPERIENCE_CHOICES),
            'qualification': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Job.QUALIFICATION_CHOICES),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Job.GENDER_CHOICES),
            'min_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter minimum salary'
            }),
            'max_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter maximum salary'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complete address'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter country'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact information'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location'
            }),
            'required_skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter required skills'
            }),
            'expired_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'dd/mm/yyyy'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'profile_image':
                self.fields[field].required = True
            self.fields[field].label = field.replace('_', ' ').title()
            if field == 'profile_image':
                self.fields[field].help_text = 'Image should be below 4mb'




from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'position_applied', 'resume', 'cover_letter']
