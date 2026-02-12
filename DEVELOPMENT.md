# Development Guide

A comprehensive guide for setting up and working with the Employee Management System in a development environment.

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Git**: Version control
- **Database**: SQLite3 (included with Python)
- **Code Editor**: VS Code, PyCharm, or similar

### Optional Tools

- **virtualenv**: For virtual environment management
- **PostgreSQL**: For production-like testing (optional)
- **Docker**: For containerized development (optional)

## Initial Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd empmanage
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt

# Optional development tools
pip install black flake8 isort pylint coverage django-debug-toolbar
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run Development Server
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

### 8. Create Test Data (Optional)
```bash
python manage.py shell
```

```python
from ems.models import User

# Create test users with different roles
User.objects.create_user(
    username='hr_user',
    password='testpass123',
    email='hr@example.com',
    role='HR',
    first_name='HR',
    last_name='Manager'
)

User.objects.create_user(
    username='manager_user',
    password='testpass123',
    email='manager@example.com',
    role='MANAGER',
    first_name='Team',
    last_name='Manager'
)

User.objects.create_user(
    username='employee_user',
    password='testpass123',
    email='employee@example.com',
    role='EMPLOYEE',
    first_name='John',
    last_name='Doe'
)

exit()
```

## Project Structure

### Core Directories

```
ems/                          # Main Django app
├── models.py                 # Data models (User, Attendance, Leave, etc.)
├── views.py                  # View logic and request handlers
├── forms.py                  # Django forms for data input
├── urls.py                   # URL routing
├── ai.py                     # AI/ML features
├── admin.py                  # Django admin configuration
├── apps.py                   # App configuration
├── migrations/               # Database schema changes
└── templates/                # HTML templates organized by feature
    ├── base.html             # Base template
    ├── dashboard.html        # Dashboard
    ├── attendance/           # Attendance feature templates
    ├── employees/            # Employee management templates
    ├── leave/                # Leave request templates
    ├── performance/          # Performance templates
    ├── salary/               # Salary templates
    ├── tasks/                # Task templates
    ├── reports/              # Report templates
    └── registration/         # Authentication templates

config/                       # Django project configuration
├── settings.py              # Project settings
├── urls.py                  # Main URL configuration
├── wsgi.py                  # WSGI application
└── asgi.py                  # ASGI application
```

## Development Workflow

### Creating a Feature

1. **Create feature branch:**
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Implement model changes (if needed):**
   Edit `ems/models.py` and create migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create forms (if needed):**
   Add form classes to `ems/forms.py`

4. **Implement views:**
   Add view functions to `ems/views.py` with proper decorators:
   ```python
   @login_required
   @role_required([User.ROLE_HR])
   def your_view(request):
       # Your logic here
       pass
   ```

5. **Add URL routes:**
   Update `ems/urls.py`:
   ```python
   path('your-route/', views.your_view, name='your-route'),
   ```

6. **Create templates:**
   Add HTML templates in appropriate directory under `ems/templates/`

7. **Add tests:**
   Create test cases in `ems/tests/` (create if doesn't exist)

8. **Test locally:**
   ```bash
   python manage.py test ems
   python manage.py runserver
   ```

9. **Commit and push:**
   ```bash
   git add .
   git commit -m "[FEATURE] Description of changes"
   git push origin feature/feature-name
   ```

10. **Create Pull Request**

### Making Database Changes

1. **Edit model:**
   ```python
   # In ems/models.py
   class MyModel(models.Model):
       new_field = models.CharField(max_length=100)
   ```

2. **Create migration:**
   ```bash
   python manage.py makemigrations ems
   ```

3. **Review migration file** in `ems/migrations/`

4. **Apply migration:**
   ```bash
   python manage.py migrate
   ```

5. **If local development, you can also:**
   ```bash
   # Reset database completely (loses all data!)
   rm db.sqlite3
   python manage.py migrate
   ```

## Testing

### Run All Tests
```bash
python manage.py test ems
```

### Run Specific Test Module
```bash
python manage.py test ems.tests.test_models
```

### Run with Coverage
```bash
pip install coverage
coverage run --source='ems' manage.py test ems
coverage report
coverage html  # Creates htmlcov/index.html
```

### Writing Tests
Create tests in `ems/tests/test_*.py`:

```python
from django.test import TestCase
from ems.models import User, AttendanceRecord

class AttendanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
    
    def test_attendance_creation(self):
        record = AttendanceRecord.objects.create(
            employee=self.user,
            status='PRESENT'
        )
        self.assertEqual(record.status, 'PRESENT')
```

## Code Quality

### Style Guide
Follow PEP 8:
```bash
flake8 ems/
```

### Format Code
```bash
black ems/ config/
```

### Check Imports
```bash
isort ems/ config/
```

### Run All Checks
```bash
flake8 ems/
black --check ems/
isort --check-only ems/
```

## Debugging

### Django Debug Toolbar
Add to installed apps (development only):
```python
INSTALLED_APPS = [
    'debug_toolbar',
    ...
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ...
]

INTERNAL_IPS = ['127.0.0.1']
```

### Python Debugger
In views:
```python
import pdb

def my_view(request):
    pdb.set_trace()  # Execution stops here
    # Step through code in console
```

### Django Shell
```bash
python manage.py shell

# In shell:
from ems.models import User
User.objects.all()
```

### Logging
Configure logging in settings.py and use:
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Database Access

### Django Admin
Visit `http://localhost:8000/admin` with superuser credentials.

Register models in `ems/admin.py`:
```python
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['field1', 'field2']
    list_filter = ['created_at']
    search_fields = ['name']
```

### Django ORM Queries
```python
from ems.models import User, AttendanceRecord

# Create
User.objects.create(username='john', email='john@example.com')

# Read
user = User.objects.get(username='john')
users = User.objects.filter(role='EMPLOYEE')
count = User.objects.count()

# Update
user.email = 'newemail@example.com'
user.save()

# Delete
user.delete()
```

## Environment Setup for Different Scenarios

### Production-like Testing
Set up PostgreSQL locally:
```bash
pip install psycopg2-binary
```

Update settings.py:
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

### Docker Setup
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Run with Docker:
```bash
docker build -t empmanage .
docker run -p 8000:8000 empmanage
```

## Useful Commands

```bash
# Database
python manage.py migrate              # Apply migrations
python manage.py makemigrations       # Create migrations
python manage.py sqlmigrate ems 0001  # Show SQL for migration

# Server
python manage.py runserver            # Start dev server
python manage.py runserver 0.0.0.0:8000  # Listen on all interfaces

# Shell
python manage.py shell                # Interactive Python shell
python manage.py shell_plus           # Enhanced shell (requires django-extensions)

# Static files
python manage.py collectstatic        # Collect static files
python manage.py findstatic           # Find where static files are

# Admin
python manage.py createsuperuser      # Create admin user
python manage.py changepassword user  # Change user password

# Testing
python manage.py test                 # Run all tests
python manage.py test ems.tests.test_models  # Run specific test

# Management
python manage.py flush                # Clear database
python manage.py dumpdata > data.json # Export data
python manage.py loaddata data.json   # Import data
```

## Troubleshooting

### Module not found
Ensure virtual environment is activated and packages are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Database errors
Reset database:
```bash
python manage.py migrate zero ems
python manage.py migrate
```

Or completely:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port already in use
Use different port:
```bash
python manage.py runserver 8001
```

### Template not found
Ensure `ems` is in INSTALLED_APPS and templates are in correct directory:
```
ems/templates/ems/template_name.html
```

## Performance Optimization

### Database Query Optimization
```python
# Use select_related for foreign keys
users = User.objects.select_related('manager')

# Use prefetch_related for reverse relations
users = User.objects.prefetch_related('tasks')

# Use only() to fetch specific fields
users = User.objects.only('username', 'email')

# Use values() for dictionary results
users = User.objects.values('username', 'email')
```

### Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def my_view(request):
    pass
```

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Git Workflow](https://git-scm.com/book/en/v2)

## Getting Help

- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- See [README.md](README.md) for project overview
- Review [SECURITY.md](SECURITY.md) for security guidelines
- Ask questions in GitHub Issues with `[QUESTION]` tag

---

Happy coding! 🚀
