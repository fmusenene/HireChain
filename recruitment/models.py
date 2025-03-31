from django.db import models

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    posted_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    experience = models.CharField(max_length=100)
    qualification = models.CharField(max_length=255)
    job_type = models.CharField(max_length=100, choices=[
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('remote', 'Remote')
    ])
    job_level = models.CharField(max_length=100, choices=[
        ('entry', 'Entry'),
        ('mid', 'Mid'),
        ('senior', 'Senior')
    ])
    gender = models.CharField(max_length=50, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('any', 'Any')
    ])
    job_expiry = models.DateField()
    skills_required = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.job_title



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
