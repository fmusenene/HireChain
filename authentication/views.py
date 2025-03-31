from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from hrm.views import *

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

class emailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        if not is_valid_email(email):
            return JsonResponse({'email_error': 'Invalid email address.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email already exists.'}, status=409)
        return JsonResponse({'email_valid': True})

class fullNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        fullName = data.get('fullName', '').strip()
        if not fullName:
            return JsonResponse({'fullName_error': 'Full name is required.'}, status=400)
        return JsonResponse({'fullName_valid': True})

class RegistrationView(View):
    def get(self, request):
        
        return render(request, 'authentication/register.html')

    def post(self, request):
        fullName = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {
            'fieldvalues': {
                'fullName': fullName,
                'email': email,
            }
        }

        # Check for mismatched passwords
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/register.html', context)

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'authentication/register.html', context)

        # Check for valid email format
        if not is_valid_email(email):
            messages.error(request, 'Invalid email format.')
            return render(request, 'authentication/register.html', context)

        try:
            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return render(request, 'authentication/register.html', context)

        # Add success message and redirect to login page
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

class VerificationView(View):
    def get(self, request):
        try:
            token = request.GET.get('token')
            user = User.objects.get(token=token)
            user.is_active = True
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            return render(request, 'authentication/register.html')
        messages.success(request, 'Account activated successfully. You can now log in.')
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('hrm')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')


