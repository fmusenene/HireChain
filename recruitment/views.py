from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Job
from .forms import JobForm
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import render
from .models import Candidate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

class JobListCreateView(ListView):
    model = Job
    template_name = 'recruitment/jobs.html'  # Updated template path
    context_object_name = 'jobs'
    ordering = ['-posted_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get date range filter
        start_date = self.request.GET.get('start_date', (timezone.now() - timedelta(days=7)).date())
        end_date = self.request.GET.get('end_date', timezone.now().date())
        
        # Get other filters
        role = self.request.GET.get('role', 'all')
        status = self.request.GET.get('status', 'all')
        sort_by = self.request.GET.get('sort_by', 'last_7_days')
        search = self.request.GET.get('search', '')
        
        # Apply filters to queryset
        queryset = self.get_queryset()
        if search:
            queryset = queryset.filter(title__icontains=search)
        if role != 'all':
            queryset = queryset.filter(category=role)
        if status != 'all':
            queryset = queryset.filter(status=status)
            
        context['jobs'] = queryset
        context['form'] = JobForm()  # Add the form to the context
        return context

def job_list(request):
    return render(request, 'recruitment/jobs.html')  # Updated template path

from django.views.generic import CreateView, ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import JobApplication
from .forms import JobApplicationForm

class JobApplicationCreateView(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'recruitment/apply.html'
    success_url = reverse_lazy('recruitment:job_applications')

    def form_valid(self, form):
        messages.success(self.request, "Application submitted successfully!")
        return super().form_valid(form)

class JobApplicationListView(ListView):
    model = JobApplication
    template_name = 'recruitment/job_list.html'
    context_object_name = 'applications'
    ordering = ['-applied_on']

class UpdateApplicationStatusView(View):
    def get(self, request, pk, status, *args, **kwargs):
        # Validate that status is allowed
        valid_statuses = dict(JobApplication._meta.get_field('status').choices).keys()
        if status not in valid_statuses:
            messages.error(request, "Invalid status")
            return redirect('recruitment:job_list')
            
        application = get_object_or_404(JobApplication, pk=pk)
        application.status = status
        application.save()
        messages.success(request, f"Application status updated to {status}.")
        return redirect('recruitment:job_list')

class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'recruitment/jobs.html'
    success_url = reverse_lazy('recruitment:job_list')

    def form_valid(self, form):
        form.instance.posted_date = timezone.now()
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error posting job. Please check the form.')
        return super().form_invalid(form)

@login_required
def candidate_list(request):
    # Get all candidates
    candidates = Candidate.objects.all()

    # Handle date filter
    date_filter = request.GET.get('date_range')
    if date_filter:
        if date_filter == 'last_7_days':
            date_threshold = datetime.now().date() - timedelta(days=7)
            candidates = candidates.filter(applied_date__gte=date_threshold)
        elif date_filter == 'last_30_days':
            date_threshold = datetime.now().date() - timedelta(days=30)
            candidates = candidates.filter(applied_date__gte=date_threshold)

    # Handle role filter
    role = request.GET.get('role')
    if role and role != 'all':
        candidates = candidates.filter(applied_role=role)

    # Handle status filter
    status = request.GET.get('status')
    if status and status != 'all':
        candidates = candidates.filter(status=status)

    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        candidates = candidates.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(cand_id__icontains=search_query) |
            Q(applied_role__icontains=search_query)
        )

    # Handle sorting
    sort_by = request.GET.get('sort_by', '-applied_date')
    candidates = candidates.order_by(sort_by)

    # Handle pagination
    rows_per_page = int(request.GET.get('rows_per_page', 10))
    paginator = Paginator(candidates, rows_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Get unique roles and statuses for filters
    all_roles = Candidate.objects.values_list('applied_role', flat=True).distinct()
    all_statuses = Candidate.objects.values_list('status', flat=True).distinct()

    context = {
        'candidates': page_obj,
        'all_roles': all_roles,
        'all_statuses': all_statuses,
        'search_query': search_query,
        'selected_role': role,
        'selected_status': status,
        'selected_date_range': date_filter,
        'rows_per_page': rows_per_page,
        'sort_by': sort_by,
    }
    
    return render(request, 'recruitment/candidate_list.html', context)
