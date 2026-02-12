from decimal import Decimal
import calendar
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_HR = 'HR'
    ROLE_MANAGER = 'MANAGER'
    ROLE_EMPLOYEE = 'EMPLOYEE'

    ROLE_CHOICES = [
        (ROLE_HR, 'HR'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_EMPLOYEE, 'Employee'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE)
    department = models.CharField(max_length=80, blank=True)
    leave_balance = models.IntegerField(default=12)

    def is_hr(self):
        return self.role == self.ROLE_HR

    def is_manager(self):
        return self.role == self.ROLE_MANAGER

    def is_employee(self):
        return self.role == self.ROLE_EMPLOYEE


class AttendanceRecord(models.Model):
    STATUS_PRESENT = 'PRESENT'
    STATUS_ABSENT = 'ABSENT'
    STATUS_LATE = 'LATE'

    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT, 'Absent'),
        (STATUS_LATE, 'Late'),
    ]

    REVIEW_PENDING = 'PENDING'
    REVIEW_APPROVED = 'APPROVED'
    REVIEW_REJECTED = 'REJECTED'

    REVIEW_CHOICES = [
        (REVIEW_PENDING, 'Pending'),
        (REVIEW_APPROVED, 'Approved'),
        (REVIEW_REJECTED, 'Rejected'),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    review_status = models.CharField(max_length=20, choices=REVIEW_CHOICES, default=REVIEW_PENDING)
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_submissions'
    )
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_reviews'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_attendance_day')
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.username} {self.date}"


class LeaveRequest(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leave_approvals'
    )
    recommended_action = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.username} {self.start_date}"

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1


class Task(models.Model):
    STATUS_ASSIGNED = 'ASSIGNED'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_DONE = 'DONE'

    STATUS_CHOICES = [
        (STATUS_ASSIGNED, 'Assigned'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_DONE, 'Done'),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_created')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ASSIGNED)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SalaryRecord(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salary_records')
    month = models.DateField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    final_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    late_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    anomaly_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month']
        constraints = [
            models.UniqueConstraint(fields=['employee', 'month'], name='unique_salary_month')
        ]

    def __str__(self):
        return f"{self.employee.username} {self.month}"

    def save(self, *args, **kwargs):
        if self.month:
            self.month = self.month.replace(day=1)
        month_start = self.month
        last_day = calendar.monthrange(self.month.year, self.month.month)[1]
        month_end = self.month.replace(day=last_day)

        attendance = AttendanceRecord.objects.filter(
            employee=self.employee,
            date__range=(month_start, month_end),
            review_status=AttendanceRecord.REVIEW_APPROVED,
        )
        self.late_days = attendance.filter(status=AttendanceRecord.STATUS_LATE).count()
        self.absent_days = attendance.filter(status=AttendanceRecord.STATUS_ABSENT).count()

        daily_rate = (self.base_salary / Decimal('22')) if self.base_salary else Decimal('0.00')
        deduction = (daily_rate * Decimal(self.absent_days)) + (daily_rate / Decimal('2')) * Decimal(self.late_days)
        self.final_salary = max(self.base_salary - deduction, Decimal('0.00'))

        previous = SalaryRecord.objects.filter(
            employee=self.employee, month__lt=self.month
        ).order_by('-month').first()
        if previous and previous.final_salary:
            diff = abs(self.final_salary - previous.final_salary)
            ratio = diff / previous.final_salary if previous.final_salary else Decimal('0.00')
            self.anomaly_flag = ratio > Decimal('0.30')
        else:
            self.anomaly_flag = False

        super().save(*args, **kwargs)


class PerformanceRating(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    month = models.DateField()
    rating = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month']
        constraints = [
            models.UniqueConstraint(fields=['employee', 'month'], name='unique_performance_month')
        ]

    def __str__(self):
        return f"{self.employee.username} {self.month}"
