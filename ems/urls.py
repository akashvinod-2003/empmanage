from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_add, name='attendance_add'),
    path('attendance/<int:pk>/review/', views.attendance_review, name='attendance_review'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/request/', views.leave_request, name='leave_request'),
    path('leave/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_add, name='task_add'),
    path('reports/', views.report_view, name='reports'),
    path('salary/', views.salary_list, name='salary_list'),
    path('salary/add/', views.salary_add, name='salary_add'),
    path('payslips/', views.payslip_list, name='payslip_list'),
    path('payslips/<int:pk>/', views.payslip_detail, name='payslip_detail'),
    path('performance/', views.performance_list, name='performance_list'),
]
