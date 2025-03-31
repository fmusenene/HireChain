from django.urls import path
from .views import job_list  # Import the function directly
from .views import JobApplicationCreateView, JobApplicationListView, UpdateApplicationStatusView

app_name = 'recruitment'

urlpatterns = [
    path('jobs/', job_list, name='job_list'),  # For listing jobs
    path('apply/', JobApplicationCreateView.as_view(), name='apply_for_job'),
    path('applications/', JobApplicationListView.as_view(), name='job_applications'),  # Changed from job_list to job_applications
    path('update_status/<int:pk>/<str:status>/', UpdateApplicationStatusView.as_view(), name='update_application_status'),
]
