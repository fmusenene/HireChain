from django.urls import path
from . import views
from .views import home, employee_list, employee_detail, edit_employee, delete_employee, about, departments, designations, policies, birthdays, holidays, leave_type, timesheets, GoalTypeView, GoalTrackingView, TrainingTypeView, TrainerListView, TrainingListView, ResignationView, TerminationListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='hrm'),  # Handles the root URL for hrm
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('employee-detail/<int:employee_id>/', views.employee_detail, name='employee_detail'),    
    path('about/', views.about, name='about'),
    path('departments/', views.departments, name='departments'),
    path('departments/edit/<int:department_id>/', views.edit_department, name='edit_department'),
    path('departments/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    path('designations/', views.designations, name='designations'),
    path('policies/', views.policies, name='policies'),
    path('birthdays/', views.birthdays, name='birthdays'),
    path('holidays/', views.holidays, name='holidays'),
    path('leave-type/', views.leave_type, name='leave_type'),
    path('leave-type/edit/<int:id>/', views.leave_type, name='leave_type_edit'),
    path('leave-type/delete/<int:id>/', views.leave_type, name='leave_type_delete'),
    path('leave-admin/', views.leave_management, name='leave_admin'),
    path('leave-employee/', views.leave_employee, name='leave_employee'),
    path('leave_employee/', views.leave_employee),  # Support underscore version
    path('timesheets/', timesheets, name='timesheets'),
    path('employee_profile/<int:employee_id>/', views.employee_profile, name='employee_profile'),
    path('admin_attendance/', views.admin_attendance, name='admin_attendance'),
    path('employee_attendance/', views.employee_attendance, name='employee_attendance'),
    path('employee_availability/', views.employee_availability, name='employee_availability'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('overtime_records/', views.overtime_records, name='overtime_records'),
    path('overtime/', views.overtime, name='overtime'),
    path('performance_indicator/', views.performance_indicator, name='performance_indicator'),
    path('performance_appraisal/', views.performance_appraisal, name='performance_appraisal'),
    path('goal-type/', GoalTypeView.as_view(), name='goal_type_view'),
    path('training-type/', TrainingTypeView.as_view(), name='training_type'),
    path("trainers/", TrainerListView.as_view(), name="trainers"),
    path('trainings/', TrainingListView.as_view(), name='training_list'),
    path('promotions/', views.PromotionListView.as_view(), name='promotion_list'),
    path("resignations/", ResignationView.as_view(), name="resignation_list"),
    path('terminations/', TerminationListView.as_view(), name='termination_list'),
    path('leave-management/', views.leave_management, name='leave_management'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)