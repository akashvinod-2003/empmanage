# Contributing to Employee Management System

Thank you for your interest in contributing to the Employee Management System! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Follow the project's coding standards
- Focus on code quality and maintainability

## Getting Started

### 1. Fork and Clone
```bash
git clone <your-fork-url>
cd empmanage
git remote add upstream <original-repo-url>
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b bugfix/description-of-bug
```

### 3. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
```

## Development Workflow

### Before Making Changes
- Check existing issues and pull requests
- Create an issue first for major features
- Discuss in the issue before starting work

### Making Changes
1. Write clear, concise commit messages
2. Follow Project Code Standards (see below)
3. Add or update tests for your changes
4. Update relevant documentation

### Testing
```bash
# Run all tests
python manage.py test ems

# Run specific test
python manage.py test ems.tests.TestCase

# Run with coverage
coverage run --source='.' manage.py test ems
coverage report
```

### Code Standards

#### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

Example:
```python
def calculate_leave_balance(user, year):
    """
    Calculate remaining leave balance for a user in given year.
    
    Args:
        user (User): The user object
        year (int): The year to calculate for
        
    Returns:
        int: Remaining leave days
    """
    # Implementation here
    pass
```

#### Django Models
- Use descriptive field names
- Add `help_text` and `verbose_name` to fields
- Include `__str__` method
- Use `Meta` class for ordering and constraints

```python
class ExampleModel(models.Model):
    name = models.CharField(
        max_length=100, 
        help_text="Employee name"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

#### Views
- Use proper authentication decorators
- Include `role_required` decorator for access control
- Add meaningful context to templates
- Handle errors gracefully

#### Templates
- Use semantic HTML
- Include proper indentation
- Use Django template tags appropriately
- Extend `base.html` for consistency

### Commit Messages

Follow this format:
```
[TYPE] Brief description (50 chars)

Extended description if needed. Explain the why, not the what.
- Point 1
- Point 2

Fixes #123
```

Types:
- `[FEATURE]` - New functionality
- `[BUGFIX]` - Bug fixes
- `[REFACTOR]` - Code refactoring
- `[DOCS]` - Documentation updates
- `[TEST]` - Test additions/updates
- `[CHORE]` - Maintenance tasks

Examples:
```
[FEATURE] Add email notification for leave approval

Implement email notifications when leave requests are
approved or rejected. Uses Django signals to trigger
notifications automatically.

Fixes #456
```

```
[BUGFIX] Fix attendance record not saving status

The AttendanceRecord model was not properly saving the
status field due to missing blank=True attribute.

Fixes #123
```

## Pull Request Process

### Before Submitting
1. Update your branch with latest main:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Run tests:
   ```bash
   python manage.py test
   ```

3. Check code style:
   ```bash
   python -m flake8 ems/ --max-line-length=100
   ```

### Submitting PR
1. Push to your fork
2. Create Pull Request against `main` branch
3. Fill out PR template completely
4. Ensure CI checks pass
5. Request review from maintainers

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing done

## Checklist
- [ ] My code follows style guidelines
- [ ] I have updated documentation
- [ ] I have added/updated tests
- [ ] No new warnings generated
```

## Reporting Bugs

### Bug Report Template
```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Screenshots**
If applicable

**Environment**
- Python version:
- Django version:
- OS:
- Browser (if applicable):

**Additional context**
Any other context
```

## Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Describe the problem

**Describe the solution you'd like**
Clear description of desired functionality

**Describe alternatives you've considered**
Other approaches

**Additional context**
Mockups, user stories, or other context
```

## Documentation

When adding features:
1. Update **README.md** with new functionality
2. Add docstrings to code
3. Update relevant section in docs
4. Document configuration changes
5. Include usage examples

## Project Structure Guidelines

```
ems/
├── models.py        # Data models
├── views.py         # View logic
├── forms.py         # Django forms
├── admin.py         # Admin configuration
├── urls.py          # URL routing
├── ai.py            # AI/ML features
└── templates/       # HTML templates
    ├── base.html
    └── [app_name]/
```

## Version Control Rules

- Never commit secrets, API keys, or passwords
- Keep commits atomic and focused
- Write meaningful commit messages
- Use feature branches, not main
- Rebase before merging
- Delete merged branches

## Code Review Process

1. **Automated Checks**
   - Tests must pass
   - Code style validated
   - No conflicts with main

2. **Manual Review**
   - Code quality assessment
   - Architecture review
   - Testing verification
   - Documentation check

3. **Feedback**
   - Constructive comments
   - Request changes if needed
   - Approve when ready

## Release Process

Versions follow Semantic Versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Getting Help

- Check existing documentation
- Search closed issues
- Ask in new issue with [QUESTION] tag
- Contact maintainers directly

## Questions?

Feel free to open an issue with tag `[QUESTION]` or contact the development team.

---

Thank you for contributing! Your efforts help make this project better for everyone. 🙏
