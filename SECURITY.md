# Security Policy

## Reporting Security Vulnerabilities

**Please do not open public GitHub issues for security vulnerabilities.**

If you discover a security vulnerability in the Employee Management System, please report it by emailing:

**akash.dev@example.com**

Include the following information in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if applicable)

We appreciate your responsible disclosure and will work to address the issue promptly.

## Security Best Practices

When deploying this application:

### Authentication & Authorization
- Always enforce strong password policies
- Keep authentication credentials secure
- Regularly rotate admin credentials
- Use HTTPS/SSL for all connections
- Implement rate limiting for login attempts
- Enable two-factor authentication in production

### Database Security
- Never use the default SQLite in production
- Use PostgreSQL or MySQL with proper access controls
- Regularly backup database
- Encrypt sensitive data fields
- Restrict database user privileges
- Keep database credentials in environment variables

### Configuration
- Set `DEBUG = False` in production
- Use a strong `SECRET_KEY` (generate new one for production)
- Keep `ALLOWED_HOSTS` restricted to your domain
- Set secure cookies: `SESSION_COOKIE_SECURE = True`
- Enable CSRF protection
- Use `.env` files for sensitive settings (never commit them)

### Deployment
- Keep Django and all dependencies updated
- Use virtual environment in production
- Run behind a reverse proxy (Nginx/Apache)
- Implement Web Application Firewall (WAF)
- Set up logging and monitoring
- Regular security audits

### Code Security
- Validate all user inputs
- Use parameterized queries (Django ORM handles this)
- Keep sensitive logs secure
- Don't log passwords or tokens
- Implement proper error handling
- Use Django's security middleware

### Access Control
- Implement role-based access control (already in place)
- Log all administrative actions
- Regularly audit user permissions
- Implement session timeout
- Disable accounts immediately upon termination
- Use audit logs for compliance

### Secrets Management
Never commit:
- Database passwords
- API keys
- Secret keys
- Email credentials
- Private keys
- Authentication tokens

Use environment variables instead:
```python
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DATABASE_PASSWORD = config('DB_PASSWORD')
```

## Dependency Security

Keep dependencies updated:
```bash
pip list --outdated
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

Use tools to scan for vulnerabilities:
```bash
pip install safety
safety check
```

## Compliance & Standards

The application should comply with:
- GDPR (for EU users)
- Local data protection regulations
- OWASP Top 10 guidelines
- PCI DSS (if handling payments)

## Version Support

| Version | Status | Support Until |
|---------|--------|---------------|
| 1.0.x   | Active | Feb 2027      |
| 0.9.x   | EOL    | Feb 2026      |

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities.
