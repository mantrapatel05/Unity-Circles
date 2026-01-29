# Unity Circles - Deployment & Final Checklist

## Pre-Launch Checklist

### Backend Setup
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Database migrations applied: `python manage.py migrate`
- [ ] Superuser created: `python manage.py createsuperuser`
- [ ] Static files configured: `python manage.py collectstatic`
- [ ] No syntax errors in Python files
- [ ] All models registered in admin
- [ ] All viewsets properly configured
- [ ] All URLs properly routed

### API Testing
- [ ] Test registration endpoint
- [ ] Test login endpoint
- [ ] Test JWT token functionality
- [ ] Test CRUD operations on all resources
- [ ] Test permissions (authenticated vs public)
- [ ] Test error handling
- [ ] Verify CORS is working
- [ ] Test file upload (profile pictures)

### Frontend Integration
- [ ] Frontend can call `/api/auth/register/`
- [ ] Frontend can call `/api/auth/token/`
- [ ] Frontend can retrieve user data with token
- [ ] JWT tokens are stored/used correctly
- [ ] All pages load correct data from API
- [ ] Forms submit data to correct endpoints
- [ ] Error messages display properly
- [ ] Loading states show during API calls

### Security
- [ ] `DEBUG = False` before production
- [ ] Generate new `SECRET_KEY` for production
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] HTTPS/SSL certificate installed
- [ ] CSRF protection enabled
- [ ] SQL injection prevention (ORM handles this)
- [ ] XSS protection enabled
- [ ] Rate limiting configured
- [ ] Sensitive data not hardcoded

### Database
- [ ] Production database configured (PostgreSQL recommended)
- [ ] Database backups setup
- [ ] Database user created with proper permissions
- [ ] Connection pooling configured (if applicable)

### Performance
- [ ] Database indexes on frequently queried fields
- [ ] Pagination implemented for list endpoints
- [ ] Caching configured (optional)
- [ ] Static files served via CDN (optional)
- [ ] Images compressed and optimized

### Monitoring & Logging
- [ ] Error logging configured
- [ ] Request logging setup
- [ ] Email alerts configured
- [ ] Uptime monitoring enabled
- [ ] Performance monitoring enabled

---

## Quick Start Commands

### Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Maintenance
```bash
# Check for security issues
python manage.py check --deploy

# Create admin user
python manage.py createsuperuser

# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json

# Clear old sessions
python manage.py clearsessions

# Collect static files
python manage.py collectstatic
```

---

## Deployment Steps

### Step 1: Server Setup
1. Rent/setup hosting (AWS, DigitalOcean, Heroku, etc.)
2. Install Python 3.8+
3. Install PostgreSQL or MySQL (recommended over SQLite)
4. Install Nginx or Apache
5. Install Supervisor/systemd for process management

### Step 2: Application Setup
```bash
# Clone repository
git clone <your-repo-url>
cd unity_circles

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment variables
cp .env.example .env
# Edit .env with production values
```

### Step 3: Configuration
Edit `unity_circles/settings.py`:
```python
DEBUG = False
SECRET_KEY = 'your-new-secret-key'
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'unity_circles_db',
        'USER': 'db_user',
        'PASSWORD': 'strong_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 4: Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 5: Web Server Setup
Configure Nginx to proxy to Django/Gunicorn

### Step 6: SSL/HTTPS
Install Let's Encrypt certificate for HTTPS

### Step 7: Process Management
Setup Supervisor/systemd to keep Django running

### Step 8: Monitoring
- Setup error tracking (Sentry)
- Enable logging
- Setup uptime monitoring

---

## Environment Variables Template

Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-random-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/unity_circles
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
FRONTEND_URL=https://yourdomain.com
```

---

## Troubleshooting Production Issues

### Issue: "DisallowedHost" Error
**Solution:** Add domain to `ALLOWED_HOSTS` in settings.py

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic` and verify Nginx configuration

### Issue: Database connection errors
**Solution:** Check database credentials and connectivity

### Issue: CORS errors
**Solution:** Add frontend domain to `CORS_ALLOWED_ORIGINS`

### Issue: 500 errors
**Solution:** Check error logs in `/var/log/` or application logs

---

## Performance Optimization

### Database
```python
# Add database indexing in models.py
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]
```

### Caching
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Compression
```python
# Add to middleware
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... other middleware
]
```

---

## Security Hardening

### Settings.py Production Config
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}
```

### Rate Limiting
```bash
pip install djangorestframework-throttling
```

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## Backup & Recovery Plan

### Daily Backups
```bash
# Backup script (run daily via cron)
#!/bin/bash
BACKUP_DIR="/backups/unity_circles"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Database backup
pg_dump unity_circles_db > $BACKUP_DIR/db_$TIMESTAMP.sql

# Application backup
tar -czf $BACKUP_DIR/app_$TIMESTAMP.tar.gz /var/www/unity_circles

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Recovery Procedure
```bash
# Restore database
psql unity_circles_db < backup.sql

# Restore application
tar -xzf app_backup.tar.gz
```

---

## Monitoring & Alerts

### Recommended Tools
- **Error Tracking:** Sentry
- **Performance:** New Relic or DataDog
- **Uptime:** Pingdom or UptimeRobot
- **Logs:** ELK Stack or Papertrail
- **APM:** Django Debug Toolbar (development only)

### Health Check Endpoint
```python
# Add to core/views.py
@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)

# Add to urls.py
path('health/', health_check)
```

---

## Scaling Considerations

### Horizontal Scaling
- Use Docker for containerization
- Deploy multiple Django instances
- Use load balancer (Nginx, HAProxy)
- Separate database from application server

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Enable caching layer
- Use CDN for static files

### Database Optimization
- Read replicas for scale-out reads
- Partitioning for large tables
- Query optimization
- Connection pooling

---

## Post-Launch Monitoring

### Daily Checks
- [ ] Server uptime
- [ ] Error rate
- [ ] Response time
- [ ] Database health
- [ ] Disk space

### Weekly Checks
- [ ] User growth
- [ ] Feature usage
- [ ] Performance trends
- [ ] Security logs

### Monthly Checks
- [ ] Dependency updates
- [ ] Performance optimization
- [ ] User feedback review
- [ ] Capacity planning

---

## Support & Contact

- **Documentation:** See README.md and API_DOCUMENTATION.md
- **Frontend Integration:** See FRONTEND_INTEGRATION.md
- **Issues:** Check SETUP_GUIDE.md troubleshooting section
- **Quick Reference:** QUICK_API_REFERENCE.md

---

**Your Unity Circles application is ready for launch!**

Follow the checklist above and refer to documentation as needed.
