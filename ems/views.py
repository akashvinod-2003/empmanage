from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .ai import attendance_flag, leave_recommendation, payslip_summary
from .forms import (
    AttendanceAdminForm,
    LeaveRequestForm,
    PerformanceRatingForm,
    SalaryRecordForm,
    TaskForm,
    UserCreateForm,
    UserUpdateForm,
)
from .models import (
    AttendanceRecord,
    LeaveRequest,
    PerformanceRating,
    SalaryRecord,
    Task,
    User,
)


def role_required(roles):
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            elevated_roles = list(roles)
            if User.ROLE_HR in roles and User.ROLE_MANAGER not in elevated_roles:
                elevated_roles.append(User.ROLE_MANAGER)
            if request.user.is_superuser or request.user.role in elevated_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('Access denied.')

        return _wrapped

    return decorator


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


class PostOnlyLogoutView(LogoutView):
    http_method_names = ['post']


@login_required
def dashboard(request):
    user = request.user
    is_admin_role = user.is_superuser or user.is_hr() or user.is_manager()
    context = {
        'role': user.role,
        'attendance_flag': attendance_flag(user) if user.is_employee() else None,
        'pending_leave_count': LeaveRequest.objects.filter(
            status=LeaveRequest.STATUS_PENDING
        ).count()
        if is_admin_role
        else LeaveRequest.objects.filter(employee=user).count(),
        'task_count': Task.objects.filter(assigned_to=user).count()
        if user.is_employee()
        else Task.objects.count(),
        'salary_alerts': SalaryRecord.objects.filter(anomaly_flag=True).count()
        if is_admin_role
        else 0,
    }
    return render(request, 'dashboard.html', context)


@login_required
@role_required([User.ROLE_HR])
def employee_list(request):
    employees = User.objects.all().order_by('username')
    return render(request, 'employees/list.html', {'employees': employees})


@login_required
@role_required([User.ROLE_HR])
def employee_add(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created.')
            return redirect('employee_list')
    else:
        form = UserCreateForm()
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add employee'})


@login_required
@role_required([User.ROLE_HR])
def employee_edit(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated.')
            return redirect('employee_list')
    else:
        form = UserUpdateForm(instance=employee)
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit employee'})


@login_required
@role_required([User.ROLE_HR])
def employee_delete(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted.')
        return redirect('employee_list')
    return render(request, 'employees/delete.html', {'employee': employee})


@login_required
def attendance_list(request):
    if request.user.is_hr() or request.user.is_manager():
        records = AttendanceRecord.objects.select_related('employee').all()
    else:
        records = AttendanceRecord.objects.filter(employee=request.user)
    return render(request, 'attendance/list.html', {'records': records})


@login_required
@role_required([User.ROLE_MANAGER, User.ROLE_HR])
def attendance_add(request):
    is_hr = request.user.is_hr()
    is_manager = request.user.is_manager()
    form_class = AttendanceAdminForm

    if request.method == 'POST':
        form = form_class(request.POST, user=request.user)
        if form.is_valid():
            record = form.save(commit=False)

            existing = AttendanceRecord.objects.filter(
                employee=record.employee, date=record.date
            ).first()
            if existing:
                existing.status = record.status
                existing.review_status = AttendanceRecord.REVIEW_APPROVED
                existing.reviewed_by = request.user
                existing.reviewed_at = timezone.now()
                existing.submitted_by = request.user
                existing.save()
                messages.success(request, 'Attendance updated and approved.')
                return redirect('attendance_list')

            record.review_status = AttendanceRecord.REVIEW_APPROVED
            record.reviewed_by = request.user
            record.reviewed_at = timezone.now()
            record.submitted_by = request.user
            record.save()
            messages.success(request, 'Attendance saved.')
            return redirect('attendance_list')
    else:
        form = form_class(user=request.user)
    return render(
        request,
        'attendance/form.html',
        {'form': form, 'is_hr': is_hr, 'is_manager': is_manager},
    )


@login_required
@role_required([User.ROLE_HR])
def attendance_review(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            record.review_status = AttendanceRecord.REVIEW_APPROVED
            record.reviewed_by = request.user
            record.reviewed_at = timezone.now()
            messages.success(request, 'Attendance approved.')
        elif action == 'reject':
            record.review_status = AttendanceRecord.REVIEW_REJECTED
            record.reviewed_by = request.user
            record.reviewed_at = timezone.now()
            messages.info(request, 'Attendance rejected.')
        record.save()
        return redirect('attendance_list')
    return render(request, 'attendance/review.html', {'record': record})


@login_required
def leave_list(request):
    if request.user.is_hr() or request.user.is_manager():
        leaves = LeaveRequest.objects.select_related('employee').all()
    else:
        leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leave/list.html', {'leaves': leaves})


@login_required
def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.recommended_action = leave_recommendation(leave)
            leave.save()
            messages.success(request, 'Leave request submitted.')
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/request.html', {'form': form})


@login_required
@role_required([User.ROLE_MANAGER, User.ROLE_HR])
def leave_approve(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            leave.status = LeaveRequest.STATUS_APPROVED
            leave.manager = request.user
            leave.employee.leave_balance = max(leave.employee.leave_balance - leave.total_days, 0)
            leave.employee.save(update_fields=['leave_balance'])
            messages.success(request, 'Leave approved.')
        elif action == 'reject':
            leave.status = LeaveRequest.STATUS_REJECTED
            leave.manager = request.user
            messages.info(request, 'Leave rejected.')
        leave.save()
        return redirect('leave_list')
    return render(request, 'leave/approve.html', {'leave': leave})


@login_required
def task_list(request):
    if request.user.is_hr() or request.user.is_manager():
        tasks = Task.objects.select_related('assigned_to').all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/list.html', {'tasks': tasks})


@login_required
@role_required([User.ROLE_MANAGER, User.ROLE_HR])
def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            messages.success(request, 'Task assigned.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/form.html', {'form': form})


@login_required
@role_required([User.ROLE_HR])
def report_view(request):
    employees = User.objects.filter(role=User.ROLE_EMPLOYEE)
    report_rows = []
    for employee in employees:
        report_rows.append(
            {
                'employee': employee,
                'attendance_flag': attendance_flag(employee),
                'leave_balance': employee.leave_balance,
                'open_tasks': Task.objects.filter(assigned_to=employee, status=Task.STATUS_ASSIGNED).count(),
            }
        )
    context = {
        'report_rows': report_rows,
        'pending_leaves': LeaveRequest.objects.filter(status=LeaveRequest.STATUS_PENDING).count(),
        'salary_anomalies': SalaryRecord.objects.filter(anomaly_flag=True).count(),
    }
    return render(request, 'reports/hr.html', context)


@login_required
@role_required([User.ROLE_HR])
def salary_list(request):
    records = SalaryRecord.objects.select_related('employee').all()
    return render(request, 'salary/list.html', {'records': records})


@login_required
@role_required([User.ROLE_HR])
def salary_add(request):
    if request.method == 'POST':
        form = SalaryRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary record saved.')
            return redirect('salary_list')
    else:
        form = SalaryRecordForm(initial={'month': date.today().replace(day=1)})
    return render(request, 'salary/form.html', {'form': form})


@login_required
def payslip_list(request):
    if request.user.is_hr() or request.user.is_manager():
        records = SalaryRecord.objects.select_related('employee').all()
    else:
        records = SalaryRecord.objects.filter(employee=request.user)
    return render(request, 'salary/payslip_list.html', {'records': records})


@login_required
def payslip_detail(request, pk):
    record = get_object_or_404(SalaryRecord, pk=pk)
    if not (request.user.is_hr() or request.user.is_manager() or record.employee == request.user):
        return HttpResponseForbidden('Access denied.')
    ai = payslip_summary(record)
    return render(request, 'salary/payslip_detail.html', {'record': record, 'ai': ai})


@login_required
def performance_list(request):
    if request.user.is_hr() or request.user.is_manager():
        ratings = PerformanceRating.objects.select_related('employee').all()
    else:
        ratings = PerformanceRating.objects.filter(employee=request.user)

    form = None
    if request.user.is_hr() or request.user.is_manager():
        if request.method == 'POST':
            form = PerformanceRatingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Performance rating saved.')
                return redirect('performance_list')
        else:
            form = PerformanceRatingForm(initial={'month': date.today().replace(day=1)})

    return render(
        request,
        'performance/list.html',
        {'ratings': ratings, 'form': form},
    )
