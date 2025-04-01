from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, JobApplication, Candidate
from .serializers import JobSerializer, JobApplicationSerializer, CandidateSerializer
from django.utils import timezone

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing job postings.
    Supports CRUD operations and custom actions.
    """
    queryset = Job.objects.all().order_by('-posted_date')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'job_type', 'job_level', 'experience', 'qualification', 'status']
    search_fields = ['title', 'description', 'required_skills']
    ordering_fields = ['posted_date', 'expired_date', 'title']

    def perform_create(self, serializer):
        """Set posted_date when creating a new job"""
        serializer.save(posted_date=timezone.now())

    @action(detail=True, methods=['post'])
    def close_job(self, request, pk=None):
        """Custom action to close a job posting"""
        job = self.get_object()
        job.status = 'closed'
        job.save()
        return Response({'status': 'job closed'})

    @action(detail=False, methods=['get'])
    def active_jobs(self, request):
        """Get all active job postings"""
        active_jobs = Job.objects.filter(
            status='active',
            expired_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(active_jobs, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Override list method to support filtering
        """
        queryset = self.get_queryset()
        
        # Apply filters
        category = request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        job_type = request.query_params.get('job_type', None)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        
        experience = request.query_params.get('experience', None)
        if experience:
            queryset = queryset.filter(experience=experience)
        
        qualification = request.query_params.get('qualification', None)
        if qualification:
            queryset = queryset.filter(qualification=qualification)

        # Serialize and return
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing job applications.
    Supports CRUD operations and custom actions.
    """
    queryset = JobApplication.objects.all().order_by('-applied_on')
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'position_applied']
    search_fields = ['full_name', 'email', 'position_applied']
    ordering_fields = ['applied_on', 'full_name']

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update application status"""
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(JobApplication._meta.get_field('status').choices):
            application.status = new_status
            application.save()
            return Response({'status': f'Application status updated to {new_status}'})
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )

class CandidateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing candidates.
    Supports CRUD operations and custom actions.
    """
    queryset = Candidate.objects.all().order_by('-applied_date')
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'applied_role']
    search_fields = ['name', 'email', 'cand_id', 'applied_role']
    ordering_fields = ['applied_date', 'name']

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update candidate status"""
        candidate = self.get_object()
        new_status = request.data.get('status')
        candidate.status = new_status
        candidate.save()
        return Response({'status': f'Candidate status updated to {new_status}'}) 