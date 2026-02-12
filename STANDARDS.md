# Project Standards & Conventions

This document outlines the coding standards and conventions used in the Employee Management System.

## Python Style Guide

### PEP 8 Compliance

All Python code must follow [PEP 8](https://pep8.org) style guide.

**Key Points:**
- 4 spaces for indentation (never tabs)
- Maximum line length: 100 characters
- Two blank lines between top-level definitions
- One blank line between method definitions
- Imports on separate lines

### Naming Conventions

```python
# Constants - UPPER_CASE
MAX_RESULTS = 100
DEFAULT_TIMEOUT = 30

# Functions and variables - lower_case_with_underscores
def calculate_leave_balance():
    employee_count = 0
    return employee_count

# Classes - PascalCase
class AttendanceRecord(models.Model):
    pass

# Private methods/attributes - _leading_underscore
def _internal_helper():
    pass

# Magic methods - __double_underscores (or __name__/__name)
class MyClass:
    def __init__(self):
        self.__private = "hidden"
```

### Imports

```python
# Standard library imports first
import calendar
from datetime import date, datetime
from decimal import Decimal

# Third-party imports
from django.contrib import messages
from django.db import models
from django.utils import timezone

# Local imports
from .models import User, AttendanceRecord
from .forms import AttendanceForm

# Import order: stdlib, third-party, local
# One import per line for clarity
# Use absolute imports, not relative (except within app)
```

### Comments & Docstrings

```python
# Good docstring
def calculate_age(birth_date):
    """
    Calculate age from birth date.
    
    Args:
        birth_date (date): The birth date
        
    Returns:
        int: Age in years
        
    Raises:
        ValueError: If birth_date is in the future
    """
    pass

# Good function comments
def complex_algorithm():
    # Check if user has permissions
    if user.is_hr():
        # Only HR can see all records
        return records
    
    # Regular users only see own records
    return records.filter(user=user)
```

## Django Conventions

### Model Definitions

```python
class User(AbstractUser):
    """Extended user model with role-based access."""
    
    ROLE_CHOICES = [
        ('HR', 'Human Resources'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='EMPLOYEE',
        help_text='User role in the system'
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text='Department assignment'
    )
    
    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_hr(self):
        """Check if user has HR role."""
        return self.role == 'HR'
```

### View Functions

```python
from django.contrib.auth.decorators import login_required
from .decorators import role_required

@login_required(login_url='login')
@role_required(['HR', 'MANAGER'])
def employee_list(request):
    """
    Display list of employees.
    
    Only accessible to HR and Manager roles.
    """
    employees = User.objects.filter(
        role='EMPLOYEE'
    ).select_related('manager')
    
    context = {
        'employees': employees,
        'total_count': employees.count(),
    }
    
    return render(request, 'employees/list.html', context)
```

### Forms

```python
class EmployeeForm(forms.ModelForm):
    """Form for creating/updating employee records."""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'department']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        """Validate email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email already exists')
        return email
```

### URL Configuration

```python
from django.urls import path
from . import views

app_name = 'ems'

urlpatterns = [
    # Always include patterns in logical groups with comments
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    # Keep patterns grouped by feature
]
```

### QuerySet Optimization

```python
# Bad: N+1 queries
def employee_list(request):
    employees = User.objects.all()
    # Template loops and accesses employee.manager → extra query per employee

# Good: Use select_related for ForeignKey
def employee_list(request):
    employees = User.objects.select_related('manager')

# Bad: Getting unnecessary fields
data = User.objects.all()  # Gets all fields

# Good: Only get needed fields
data = User.objects.values_list('username', 'email')
data = User.objects.only('username', 'email')

# Bad: Multiple calls
users = User.objects.filter(role='EMPLOYEE')
count = User.objects.filter(role='EMPLOYEE').count()

# Good: Single query
users = User.objects.filter(role='EMPLOYEE')
count = users.count()  # Uses cached count
```

## Template Conventions

```html
{% extends "base.html" %}

{% block title %}Employee List{% endblock %}

{% block content %}
<div class="container">
    {% if messages %}
        <div class="alerts">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        </div>
    {% endif %}
    
    <!-- Always use descriptive variable names -->
    {% if employee_list %}
        <table class="table">
            {% for employee in employee_list %}
                <tr>
                    <td>{{ employee.get_full_name }}</td>
                    <td>{{ employee.get_role_display }}</td>
                    <td>
                        {% if perms.ems.change_user %}
                            <a href="{% url 'employee_edit' employee.pk %}">Edit</a>
                        {% endif %}
                    </td>
                </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>No employees found.</p>
    {% endif %}
</div>
{% endblock %}
```

## Test Conventions

```python
from django.test import TestCase
from ems.models import User, AttendanceRecord

class AttendanceRecordTestCase(TestCase):
    """Tests for AttendanceRecord model."""
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level test data."""
        super().setUpClass()
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='EMPLOYEE'
        )
    
    def setUp(self):
        """Set up test data before each test."""
        self.record = AttendanceRecord.objects.create(
            employee=self.test_user,
            date='2024-01-15',
            status='PRESENT'
        )
    
    def test_attendance_record_creation(self):
        """Test creating attendance record."""
        self.assertEqual(self.record.status, 'PRESENT')
        self.assertEqual(self.record.employee, self.test_user)
    
    def test_attendance_record_str(self):
        """Test string representation."""
        expected = f"{self.test_user.username} - 2024-01-15"
        self.assertEqual(str(self.record), expected)
    
    def tearDown(self):
        """Clean up after each test."""
        self.record.delete()
```

## Git Conventions

### Commit Messages

```
[TYPE] Short description (50 chars max)

Longer explanation if needed. Explain the WHY, not the WHAT.

- Point 1
- Point 2

Breaking changes:
BREAKING CHANGE: description of what changed

Fixes #123
Relates to #456
```

**Types:**
- `[FEATURE]` - New functionality
- `[BUGFIX]` - Bug fixes
- `[REFACTOR]` - Code refactoring
- `[DOCS]` - Documentation
- `[TEST]` - Tests
- `[CHORE]` - Maintenance

### Branch Names

```
feature/user-authentication
bugfix/attendance-status-error
refactor/model-optimization
docs/update-readme
test/add-coverage
hotfix/critical-bug
```

## Code Organization

### File Structure
```
ems/
├── models.py          # Keep under 500 lines, split if needed
├── views.py           # Group related views, split at ~300 lines
├── forms.py           # Group related forms
├── urls.py            # Keep organized with comments
├── admin.py           # Admin configuration
├── ai.py              # AI/ML functions
├── decorators.py      # Custom decorators (optional)
├── managers.py        # Custom managers (optional)
├── utils.py           # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_utils.py
└── migrations/        # Auto-generated
```

### Constants Organization

```python
# In models.py or a dedicated constants.py

class AttendanceStatus:
    """Attendance status choices."""
    PRESENT = 'PRESENT'
    ABSENT = 'ABSENT'
    LATE = 'LATE'
    
    CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
    ]

class UserRole:
    """User role choices."""
    HR = 'HR'
    MANAGER = 'MANAGER'
    EMPLOYEE = 'EMPLOYEE'
    
    CHOICES = [
        (HR, 'HR'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
    ]
```

## Documentation Standards

### README Sections
- Features overview
- Installation instructions
- Usage guide
- Configuration
- Deployment guide

### Code Comments
- Avoid obvious comments
- Explain WHY, not WHAT
- Keep comments updated
- Use docstrings for modules, functions, and classes

### Docstring Format (Google style)
```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1 (type): Description
        param2 (type): Description
        
    Returns:
        type: Description of return value
        
    Raises:
        ExceptionType: When and why raised
        
    Example:
        >>> function_name('value', 42)
        'result'
    """
    pass
```

## Performance Guidelines

### Database Query Optimization
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for reverse relations
- Use indexes for frequently queried fields
- Avoid N+1 queries
- Limit queryset results for large tables

### Caching
- Cache expensive queries
- Cache template fragments
- Cache paginated lists
- Document cache invalidation

### Code Optimization
- Minimize function calls in templates
- Use `only()` or `values()` to limit fields
- Batch database operations
- Use F() expressions for database calculations

## Security Guidelines

### User Input
```python
# Always validate and sanitize
form = MyForm(request.POST)
if form.is_valid():
    # Use cleaned_data
    data = form.cleaned_data['field']
```

### Authentication
- Use `@login_required` on all views
- Use `@role_required` for role-based views
- Never trust user input
- Always check permissions

### Data Protection
```python
# Don't log passwords
logger.info(f"User login attempted for {username}")  # Good
logger.info(f"Password is {password}")  # NEVER!

# Use Django's permission system
if request.user.has_perm('ems.view_salary'):
    # Allow viewing
    pass
```

## Linting & Formatting

All code must pass:

```bash
# PEP8 compliance
flake8 ems/ --max-line-length=100

# Code formatting
black ems/

# Import sorting
isort ems/

# Type checking (if using type hints)
mypy ems/
```

## Tools & IDE Configuration

### VS Code Settings
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length=100"],
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.python",
        "editor.formatOnSave": true
    }
}
```

### Pre-commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
black ems/ config/
isort ems/ config/
flake8 ems/ config/
python manage.py test
```

---

For detailed development instructions, see [DEVELOPMENT.md](DEVELOPMENT.md)
