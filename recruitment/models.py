from django.db import models
from django.utils import timezone

class Job(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('remote', 'Remote'),
    ]
    
    JOB_LEVEL_CHOICES = [
        ('entry', 'Entry'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('any', 'Any'),
    ]

    CATEGORY_CHOICES = [
        ('it', 'Information Technology'),
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('engineering', 'Engineering'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]

    QUALIFICATION_CHOICES = [
        ('high_school', 'High School'),
        ('bachelors', "Bachelor's Degree"),
        ('masters', "Master's Degree"),
        ('phd', 'PhD'),
        ('certification', 'Professional Certification'),
        ('diploma', 'Diploma'),
        ('other', 'Other'),
    ]

    EXPERIENCE_CHOICES = [
        ('0-1', '0-1 Years'),
        ('1-3', '1-3 Years'),
        ('3-5', '3-5 Years'),
        ('5-7', '5-7 Years'),
        ('7-10', '7-10 Years'),
        ('10+', '10+ Years'),
    ]

    profile_image = models.ImageField(upload_to='job_profiles/', max_length=255, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    job_level = models.CharField(max_length=20, choices=JOB_LEVEL_CHOICES)
    experience = models.CharField(max_length=100, choices=EXPERIENCE_CHOICES)
    qualification = models.CharField(max_length=200, choices=QUALIFICATION_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    contact = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=100, null=True, blank=True)
    required_skills = models.TextField(blank=True)
    expired_date = models.DateField()
    posted_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return self.title



# Choices for application status
STATUS_CHOICES = [
    ('sent', 'Sent'),
    ('scheduled', 'Scheduled'),
    ('interviewing', 'Interviewing'),
    ('offered', 'Offered'),
    ('hired', 'Hired'),
    ('rejected', 'Rejected'),
]

class JobApplication(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    position_applied = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes/')  # Upload resumes
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.position_applied} ({self.status})"

class Candidate(models.Model):
    cand_id = models.CharField(max_length=10, unique=True)  # For storing Cand-001 format
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    applied_role = models.CharField(max_length=100)
    applied_date = models.DateField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    status = models.CharField(max_length=20, default='Sent')

    def save(self, *args, **kwargs):
        if not self.cand_id:
            # Get the last ID and increment
            last_candidate = Candidate.objects.order_by('-cand_id').first()
            if last_candidate:
                last_id = int(last_candidate.cand_id.split('-')[1])
                self.cand_id = f'Cand-{str(last_id + 1).zfill(3)}'
            else:
                self.cand_id = 'Cand-001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cand_id} - {self.name}"
