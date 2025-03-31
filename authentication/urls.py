from .views import RegistrationView, emailValidationView, fullNameValidationView, login_view, logout_view
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

app_name = 'authentication'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),  # Added trailing slash
    path('login/', csrf_exempt(login_view), name='login'),
    path('logout/', csrf_exempt(logout_view), name='logout'),
    path('validate-email/', csrf_exempt(emailValidationView.as_view()), name="validate_email"),
    path('validate-fullName/', csrf_exempt(fullNameValidationView.as_view()), name="validate_fullName"),
]
