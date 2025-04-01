from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobListCreateView, 
    JobApplicationCreateView, 
    JobApplicationListView, 
    UpdateApplicationStatusView, 
    JobCreateView,
    candidate_list
)
from .api_views import JobViewSet, JobApplicationViewSet, CandidateViewSet

app_name = 'recruitment'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', JobApplicationViewSet)
router.register(r'candidates', CandidateViewSet)

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job_list'),  # Updated to use JobListCreateView
    path('jobs/post/', JobCreateView.as_view(), name='post_job'),
    path('apply/', JobApplicationCreateView.as_view(), name='apply_for_job'),
    path('applications/', JobApplicationListView.as_view(), name='job_applications'),
    path('update_status/<int:pk>/<str:status>/', UpdateApplicationStatusView.as_view(), name='update_application_status'),
    path('candidates/', candidate_list, name='candidate_list'),
    
    # API URLs
    path('api/', include(router.urls)),
]
