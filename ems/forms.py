from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User,
    AttendanceRecord,
    LeaveRequest,
    Task,
    SalaryRecord,
    PerformanceRating,
)


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'department',
            'leave_balance',
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'role',
            'department',
            'leave_balance',
        )


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ('date', 'status')
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class AttendanceAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        queryset = User.objects.filter(role=User.ROLE_EMPLOYEE).order_by('username')
        self.fields['employee'].queryset = queryset

    class Meta:
        model = AttendanceRecord
        fields = ('employee', 'date', 'status')
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ('start_date', 'end_date', 'reason')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'assigned_to', 'due_date')
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}


class SalaryRecordForm(forms.ModelForm):
    class Meta:
        model = SalaryRecord
        fields = ('employee', 'month', 'base_salary')
        widgets = {'month': forms.DateInput(attrs={'type': 'date'})}


class PerformanceRatingForm(forms.ModelForm):
    class Meta:
        model = PerformanceRating
        fields = ('employee', 'month', 'rating', 'notes')
        widgets = {'month': forms.DateInput(attrs={'type': 'date'})}
