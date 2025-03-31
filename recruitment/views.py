from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Job
from .forms import JobForm

class JobListCreateView(ListView, CreateView):
    model = Job
    template_name = 'recruitment/job.html'  # Ensure this is correctly set
    context_object_name = 'jobs'
    form_class = JobForm
    success_url = reverse_lazy('recruitment:job_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JobForm()
        return context

from django.shortcuts import render

def job_list(request):
    return render(request, 'recruitment/job.html')  # Make sure 'job.html' exists



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
