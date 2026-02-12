from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    AttendanceRecord,
    LeaveRequest,
    Task,
    SalaryRecord,
    PerformanceRating,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('EMS', {'fields': ('role', 'department', 'leave_balance')}),
    )
    list_display = ('username', 'email', 'role', 'department', 'is_staff')
    list_filter = ('role', 'department')


admin.site.register(AttendanceRecord)
admin.site.register(LeaveRequest)
admin.site.register(Task)
admin.site.register(SalaryRecord)
admin.site.register(PerformanceRating)
