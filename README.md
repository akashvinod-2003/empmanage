# Employee Management System (EMS)

A comprehensive Django-based employee management system with role-based access control, attendance tracking, leave management, performance ratings, and AI-powered insights.

## Features

### 👥 User Management
- **Role-Based Access Control**: HR, Manager, and Employee roles with granular permissions
- **Employee Profiles**: Department assignment, leave balance tracking
- **User Authentication**: Secure login and session management

### 📋 Attendance Management
- **Attendance Records**: Track daily attendance with status (Present, Absent, Late)
- **Review Workflow**: Pending reviews for attendance anomalies
- **AI-Powered Flagging**: Automatic detection of unusual attendance patterns
- **Admin Dashboard**: Comprehensive attendance oversight

### 🏝️ Leave Management
- **Leave Requests**: Submit and manage leave applications
- **Leave Balance**: Automatic tracking and deduction
- **AI Recommendations**: Smart leave approval suggestions
- **Approval Workflow**: Manager and HR approval process

### ⭐ Performance Management
- **Performance Ratings**: Track employee performance metrics
- **Rating Management**: Add and update performance evaluations
- **Historical Records**: Maintain performance history

### 💰 Salary Management
- **Salary Records**: Manage employee salaries and compensation
- **Payslip Generation**: Create and view detailed payslips
- **Anomaly Detection**: AI-powered detection of salary anomalies
- **Financial Reports**: HR-ready salary reports

### 📊 Task Management
- **Task Assignment**: Assign tasks to employees
- **Task Tracking**: Monitor task status and progress
- **Employee Task View**: Personal task dashboard

### 📈 Reports & Analytics
- **HR Reports**: Comprehensive salary and attendance reports
- **Data Export**: Generate reports for analysis

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite3
- **Frontend**: Django Templates with CSS styling
- **AI/ML**: Integrated AI module for intelligent recommendations
- **Authentication**: Django built-in authentication system

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd empmanage
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000`

## Project Structure

```
empmanage/
├── config/                 # Django configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── ems/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URL routing
│   ├── ai.py              # AI/ML features
│   ├── admin.py           # Django admin config
│   ├── templates/         # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── attendance/
│   │   ├── employees/
│   │   ├── leave/
│   │   ├── performance/
│   │   ├── salary/
│   │   ├── tasks/
│   │   ├── reports/
│   │   └── registration/
│   ├── static/            # CSS and static files
│   └── migrations/        # Database migrations
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database
└── README.md             # This file
```

## Usage Guide

### User Roles & Permissions

#### HR Role
- Manage all employees
- Approve/reject leave requests
- View attendance records
- Generate reports
- Access all salary information
- Manage performance ratings

#### Manager Role
- View team attendance
- Approve department's leave requests
- Assign and track tasks
- View team performance

#### Employee Role
- View personal attendance
- Submit leave requests
- View assigned tasks
- Access personal payslips

### Key Workflows

#### Adding an Employee (HR Only)
1. Navigate to Employees → Add Employee
2. Fill in employee details (name, email, department, role)
3. System generates temporary password
4. Employee logs in and updates password

#### Recording Attendance
1. Go to Attendance → Record Attendance
2. Select date and employee(s)
3. Mark as Present, Absent, or Late
4. Submit for review if anomaly detected

#### Leave Request Process
1. Employee submits leave request
2. Manager reviews and approves/rejects
3. HR receives notification
4. AI provides leave balance recommendation

#### Generating Payslips
1. Go to Salary Management
2. Create salary record
3. System generates payslip with deductions
4. AI flags any salary anomalies

## API Endpoints

The application uses Django's function-based views. All endpoints require authentication based on user role.

### Attendance
- `GET /attendance/` - List attendance
- `POST /attendance/record/` - Record new attendance
- `GET /attendance/<id>/review/` - Review attendance

### Employees
- `GET /employees/` - List all employees
- `POST /employees/add/` - Create employee
- `GET /employees/<id>/edit/` - Edit employee

### Leave
- `GET /leave/` - List leave requests
- `POST /leave/request/` - Submit leave request
- `GET /leave/<id>/approve/` - Approve leave

### Salary
- `GET /salary/` - List salaries
- `POST /salary/add/` - Add salary record
- `GET /salary/payslip/<id>/` - View payslip

### Tasks
- `GET /tasks/` - List tasks
- `POST /tasks/` - Create task

## AI Features

### Attendance Flagging
Automatically identifies suspicious attendance patterns:
- Unusual frequency of absences
- Late arrival patterns
- Attendance inconsistencies

### Leave Recommendations
AI suggests optimal leave approval based on:
- Leave balance
- Historical patterns
- Team availability
- Business impact

### Payslip Summaries
Generates intelligent summaries highlighting:
- Salary anomalies
- Deduction patterns
- Trend analysis

## Configuration

### Email Settings (Optional)
To enable email notifications, update `config/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-email-provider'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Database
Currently uses SQLite3. For production, switch to PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'empmanage',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Troubleshooting

### Common Issues

**Issue: "No module named 'ems'"**
- Solution: Ensure you're in the correct directory and the virtual environment is activated

**Issue: Database error after migration**
- Solution: Delete `db.sqlite3` and run `python manage.py migrate` again

**Issue: Static files not loading**
- Solution: Run `python manage.py collectstatic` in production

**Issue: Permission denied error**
- Solution: Check user role matches required permissions for the view

## Development

### Running Tests
```bash
python manage.py test ems
```

### Creating Migrations
After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Admin
Access Django admin at `http://localhost:8000/admin` with superuser credentials.

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Generate secure `SECRET_KEY`
- [ ] Switch to production database (PostgreSQL recommended)
- [ ] Configure email backend
- [ ] Set up HTTPS/SSL
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure environment variables

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is proprietary software by Akash. All rights reserved. See [LICENSE](LICENSE) for details.

## Support

For issues, questions, or feature requests, please contact the developer or create an issue in the repository.

## Changelog

### Version 1.0.0 (Current)
- Initial release with core features
- Role-based access control
- Attendance management system
- Leave request workflow
- Performance and salary management
- AI-powered recommendations
- Task management system

## Acknowledgments

Built as a freelance project by Akash. Special thanks to all contributors and users.

---

**Last Updated**: February 2026
**Status**: Production Ready
