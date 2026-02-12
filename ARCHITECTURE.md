# Architecture Overview

This document describes the high-level architecture and design decisions of the Employee Management System.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Users (Browsers)                     │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                   Nginx/Apache (Reverse Proxy)           │
│                      (Production)                        │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                    Django Web Server                      │
│              (Gunicorn/uWSGI in Production)              │
└────────────┬──────────────────────────────┬─────────────┘
             │                              │
     ┌───────▼─────────┐         ┌──────────▼──────────┐
     │   Django ORM    │         │   Static Files      │
     │   & Views       │         │   CSS, JS, Images   │
     │                 │         │                     │
     │ - Authentication│         └─────────────────────┘
     │ - Permissions   │
     │ - Business Logic│
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │    Database     │
     │   SQLite/PG     │
     └─────────────────┘
```

## Module Organization

### `ems/models.py` - Data Layer
Defines all database models:

```
User
├── ROLE_HR
├── ROLE_MANAGER
├── ROLE_EMPLOYEE
└── is_hr(), is_manager(), is_employee()

AttendanceRecord
├── STATUS_PRESENT/ABSENT/LATE
├── REVIEW_PENDING/APPROVED/REJECTED
└── Foreign Key → User

LeaveRequest
├── STATUS_PENDING/APPROVED/REJECTED
├── Leave type, duration
└── Foreign Keys → User

Task
├── Status tracking
├── Assignment to users
└── Foreign Keys → User

PerformanceRating
├── Rating scores
└── Foreign Keys → User

SalaryRecord
├── Salary details
├── Deductions
├── Anomaly detection
└── Foreign Keys → User
```

### `ems/views.py` - Business Logic Layer
Request handlers with role-based access:

```
Authentication Views
├── home()
├── login() [via Django]
└── PostOnlyLogoutView()

Dashboard
└── dashboard() - Role-aware dashboard

Employee Management [HR only]
├── employee_list()
├── employee_add()
├── employee_edit()
└── employee_delete()

Attendance [All roles]
├── attendance_list() - Filtered by role
├── attendance_record() - HR/Manager
├── attendance_review() - HR/Manager
└── attendance_detail()

Leave Management [All roles]
├── leave_list()
├── leave_request() - Employees
├── leave_approve() - HR/Manager
└── leave_detail()

Performance Management [HR/Manager]
├── performance_list()
└── performance_rating()

Salary Management [HR only]
├── salary_list()
├── salary_add()
├── salary_detail()
├── payslip_list()
└── payslip_detail()

Task Management [All roles]
├── task_list() - Filtered by role
├── task_add() [Manager/HR]
└── task_detail()
```

### `ems/forms.py` - Form Layer
Django form classes for data validation:

- `UserCreateForm` - User registration
- `UserUpdateForm` - Profile updates
- `AttendanceAdminForm` - Attendance records
- `LeaveRequestForm` - Leave applications
- `TaskForm` - Task creation
- `SalaryRecordForm` - Salary data
- `PerformanceRatingForm` - Ratings

### `ems/ai.py` - AI/ML Features
Intelligent features:

```python
attendance_flag(user)        # Detects unusual patterns
leave_recommendation(data)   # Predicts optimal approvals
payslip_summary(record)      # Analyzes salary data
```

## Authentication & Authorization

### Django Authentication
- Built-in user authentication system
- Session-based (not token-based)
- CSRF protection enabled

### Role-Based Access Control (RBAC)

```python
@login_required                      # Requires authentication
@role_required([User.ROLE_HR])      # HR users only

@role_required([User.ROLE_MANAGER])  # HR + Manager (elevated)
```

### Role Hierarchy
```
HR ──┐
     ├─→ Can approve most actions
     │    Can access all data
     │    Can generate reports
     │
Manager──┐
     │    Can approve in their department
     │    Can view team data
     │
Employee → Can view own data only
```

## Database Schema

### Key Relationships

```
User (extends AbstractUser)
  ├── 1:M → AttendanceRecord
  ├── 1:M → LeaveRequest
  ├── 1:M → Task (assigned_to)
  ├── 1:M → PerformanceRating
  └── 1:M → SalaryRecord

AttendanceRecord
  ├── ForeignKey → User
  ├── DateField → date
  └── CharField → status

LeaveRequest
  ├── ForeignKey → User (employee)
  ├── ForeignKey → User (approved_by, nullable)
  ├── DateField → start_date, end_date
  └── CharField → status

Task
  ├── ForeignKey → User (created_by)
  ├── ForeignKey → User (assigned_to)
  └── CharField → status

PerformanceRating
  ├── ForeignKey → User (employee)
  ├── ForeignKey → User (rated_by)
  └── DecimalField → rating

SalaryRecord
  ├── ForeignKey → User
  ├── DecimalField → basic_salary
  ├── DecimalField → deductions
  ├── BooleanField → anomaly_flag
  └── DateField → month

```

## URL Routing Structure

```
/                                    # Home → Dashboard
/admin/                             # Django Admin
/auth/
  ├── login/                        # Login page
  ├── logout/                       # Logout (POST only)
  └── dashboard/                    # Dashboard

/employees/
  ├── (list) [HR]                   # List all employees
  ├── add/ [HR]                     # Add employee
  ├── <id>/edit/ [HR]               # Edit employee
  └── <id>/delete/ [HR]             # Delete employee

/attendance/
  ├── (list) [All]                  # View attendance
  ├── record/ [HR/Manager]          # Record attendance
  ├── <id>/review/ [HR/Manager]     # Review attendance
  └── <id>/detail/ [All]            # View details

/leave/
  ├── (list) [All]                  # View requests
  ├── request/ [Employees]          # Submit request
  ├── <id>/approve/ [HR/Manager]    # Approve request
  └── <id>/detail/ [All]            # View details

/performance/
  ├── (list) [HR/Manager]           # View ratings
  └── <id>/rate/ [HR/Manager]       # Add rating

/salary/
  ├── (list) [HR]                   # View salaries
  ├── add/ [HR]                     # Add salary
  ├── <id>/detail/ [HR]             # View salary details
  ├── payslips/ [All]               # View payslips
  └── payslip/<id>/ [All]           # View payslip details

/tasks/
  ├── (list) [All]                  # View tasks
  ├── create/ [HR/Manager]          # Create task
  └── <id>/detail/ [All]            # View task
```

## Template Hierarchy

```
base.html (Base layout, navigation)
├── dashboard.html (Role-aware dashboard)
├── registration/login.html
├── attendance/
│   ├── list.html (Filtered by role)
│   ├── form.html (Record attendance)
│   └── review.html (Approve attendance)
├── employees/
│   ├── list.html
│   ├── form.html
│   └── delete.html
├── leave/
│   ├── list.html
│   ├── request.html
│   ├── approve.html
│   └── list.html
├── performance/
│   └── list.html
├── salary/
│   ├── list.html
│   ├── form.html
│   ├── payslip_list.html
│   └── payslip_detail.html
├── tasks/
│   ├── list.html
│   └── form.html
└── reports/
    └── hr.html
```

## Data Flow Examples

### Leave Request Workflow
```
1. Employee submits form
   ↓
2. LeaveRequestForm validates data
   ↓
3. View creates LeaveRequest object (status=PENDING)
   ↓
4. Notification to manager
   ↓
5. Manager reviews and updates status
   ↓
6. AI evaluates recommendation
   ↓
7. HR approves/rejects
   ↓
8. Employee notified of decision
   ↓
9. If approved, leave_balance updated
```

### Attendance Recording
```
1. HR/Manager submits attendance form
   ↓
2. AttendanceAdminForm validates data
   ↓
3. System creates AttendanceRecord
   ↓
4. AI flag feature enables anomaly detection
   ↓
5. If anomalous, mark review_status=PENDING
   ↓
6. HR reviews flagged records
   ↓
7. HR approves/rejects record
   ↓
8. History maintained for audit
```

## Security Considerations

### Authentication
- CSRF tokens on all forms
- Secure password hashing (Django default)
- Session timeout configurable
- Login required decorator on sensitive views

### Authorization
- `@role_required` decorator on views
- Database-level constraints
- Queryset filtering by user role

### Data Protection
- Password-protected admin panel
- User data isolated by role
- Audit trail for sensitive actions
- Input validation on all forms

## Scalability Considerations

### Current State (SQLite)
- Suitable for small teams (< 500 employees)
- Fine for development
- Limited concurrent users

### Scaling to Production
1. **Database**: Migrate to PostgreSQL
2. **Server**: Use Gunicorn + Nginx
3. **Caching**: Redis for sessions/cache
4. **Static Files**: CDN or S3 for media
5. **Monitoring**: Add logging and monitoring
6. **Load Balancer**: For multiple server instances

### Future Enhancements
- API layer (Django REST Framework)
- Async tasks (Celery)
- Real-time notifications (WebSockets)
- Mobile app (React Native)
- Advanced analytics (BI integration)

## Deployment Architecture

```
Production Environment:

Users
  ↓
CDN (Static files)
  ↓
Load Balancer
  ↓
┌─────────────────────────────┐
│ Nginx (Reverse Proxy)       │
│ - SSL/TLS termination       │
│ - Request routing           │
│ - Compression               │
└──────────┬──────────────────┘
           ↓
┌──────────┴──────────┐
│                     │
Gunicorn           Gunicorn
Workers            Workers
(Django)           (Django)
│                     │
└──────────┬──────────┘
           ↓
Database (PostgreSQL)
```

## Performance Optimization Strategies

1. **Query Optimization**
   - `select_related()` for ForeignKeys
   - `prefetch_related()` for reverse relations
   - Index frequently searched fields

2. **Caching**
   - Page caching with Redis
   - Queryset caching
   - View-level caching

3. **Pagination**
   - Limit result sets
   - Lazy loading for large tables

4. **Database**
   - Connection pooling
   - Query optimization
   - Regular maintenance

## Testing Strategy

### Unit Tests
```python
# Test individual models and functions
- Model validation
- Business logic
- AI features
```

### Integration Tests
```python
# Test workflows
- View requests
- Form submissions
- Database operations
```

### End-to-End Tests
```python
# Test user journeys
- Complete leave request process
- Attendance workflow
- Report generation
```

## Development Best Practices

1. **Version Control**
   - Feature branches
   - Meaningful commits
   - Pull request reviews

2. **Code Quality**
   - PEP 8 compliance
   - DRY principles
   - Comprehensive documentation

3. **Testing**
   - Write tests first (TDD preferred)
   - Maintain > 80% coverage
   - Automate tests in CI/CD

4. **Documentation**
   - Docstrings on functions
   - README updates
   - Architecture documentation

---

For implementation details, see [DEVELOPMENT.md](DEVELOPMENT.md)
