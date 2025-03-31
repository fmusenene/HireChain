from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Employee

@receiver(post_migrate)
def set_default_profile_images(sender, **kwargs):
    # Code to set the default profile image for employees
    for employee in Employee.objects.filter(profile_image__isnull=True):
        employee.profile_image = 'profile_images/default_profile.png'
        employee.save()

