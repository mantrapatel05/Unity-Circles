# Unity Circles - Complete Setup Guide

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Step 1: Install Dependencies

```bash
cd path/to/unity_circles
pip install -r requirements.txt
```

**Packages Installed:**
- Django 6.0.1 - Web framework
- djangorestframework 3.14.0 - REST API framework
- django-cors-headers 4.3.1 - CORS support for frontend
- djangorestframework-simplejwt 5.3.2 - JWT authentication
- Pillow 10.1.0 - Image processing

## Step 2: Database Setup

### Create and Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the database with all required tables:
- auth_user (Django built-in)
- accounts_studentprofile
- core_community
- chat_chatroom
- chat_message
- mentorship_mentorshiprequest
- mentorship_mentorship
- onboarding_onboardingstep

## Step 3: Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. You'll use this to access `/admin/`.

## Step 4: Run the Server

```bash
python manage.py runserver
```

Server will start at: `http://127.0.0.1:8000/`

## Project Layout & File Structure

### Core Configuration Files

**`unity_circles/settings.py`**
- Database configuration
- Installed apps
- Middleware setup
- CORS configuration
- Static files settings
- JWT token settings

**`unity_circles/urls.py`**
- Main URL router
- Includes all app URLs under API routes
- Serves static and media files

**`manage.py`**
- Django management script for running commands

### Apps & Their Purposes

#### 1. **accounts/** - User Authentication & Profiles
- `models.py`: StudentProfile model with user roles (student/mentor/both)
- `views.py`: Registration, profile management, current user endpoint
- `serializers.py`: Convert models to/from JSON
- `urls.py`: Auth endpoints (/api/auth/)
- `admin.py`: Django admin configuration

Key Endpoints:
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/token/` - Get JWT token
- GET `/api/auth/me/` - Get current user
- GET/POST `/api/auth/profile/` - User profile management

#### 2. **core/** - Communities Management
- `models.py`: Community model with members and categories
- `views.py`: Community CRUD + template rendering
- `serializers.py`: Community serialization
- `urls.py`: Community endpoints + page routing
- `admin.py`: Admin configuration

Key Endpoints:
- GET/POST `/api/communities/` - List/create communities
- GET/PUT/DELETE `/api/communities/{id}/` - Community management

#### 3. **chat/** - Messaging System
- `models.py`: ChatRoom and Message models
- `views.py`: Chat operations
- `serializers.py`: Chat serialization
- `urls.py`: Chat endpoints
- `admin.py`: Admin configuration

Key Endpoints:
- GET/POST `/api/chat/rooms/` - Chat room management
- GET/POST `/api/chat/messages/` - Message management

#### 4. **mentorship/** - Mentorship Features
- `models.py`: MentorshipRequest and Mentorship models
- `views.py`: Handle requests, acceptances, and active mentorships
- `serializers.py`: Mentorship serialization
- `urls.py`: Mentorship endpoints
- `admin.py`: Admin configuration

Key Endpoints:
- GET/POST `/api/mentorship/requests/` - Mentorship requests
- POST `/api/mentorship/requests/{id}/accept/` - Accept mentorship
- POST `/api/mentorship/requests/{id}/reject/` - Reject mentorship

#### 5. **onboarding/** - User Onboarding
- `models.py`: OnboardingStep model tracking completion
- `views.py`: Handle onboarding progress
- `serializers.py`: Onboarding serialization
- `urls.py`: Onboarding endpoints
- `admin.py`: Admin configuration

Key Endpoints:
- GET `/api/onboarding/steps/` - Get progress
- POST `/api/onboarding/steps/{id}/complete_profile/` - Mark steps complete

### Frontend Files (Connected to Backend)

**`templates/` - HTML Files**
- `landing.html` - Home page (routes to `/`)
- `signup.html` - Registration (connects to `/api/auth/register/`)
- `login.html` - Login page (connects to `/api/auth/token/`)
- `dashboard.html` - Main dashboard (requires auth)
- `profile.html` - User profile (connects to `/api/auth/profile/`)
- `communities.html` - Communities (connects to `/api/communities/`)
- `mentors.html` - Mentorship (connects to `/api/mentorship/`)
- `messages.html` - Chat (connects to `/api/chat/`)
- `meetings.html` - Meetings (connects to community + mentorship)
- `onboarding.html` - Onboarding flow (connects to `/api/onboarding/`)

**`static/` - Static Assets**
- `css/styles.css` - Styling
- `js/main.js` - Frontend logic

## API Usage Examples

### 1. Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Get JWT Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Use Token to Access Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 4. Create a Community
```bash
curl -X POST http://localhost:8000/api/communities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Python Developers",
    "description": "A community for Python developers",
    "category": "tech"
  }'
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'rest_framework'"
**Solution**: Run `pip install -r requirements.txt`

### Error: "django.db.utils.OperationalError: no such table"
**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Error: CORS issues from frontend
**Solution**: Check CORS_ALLOWED_ORIGINS in settings.py and ensure your frontend URL is listed.

### Error: "authentication credentials were not provided"
**Solution**: Ensure you're including the Authorization header with JWT token in API requests.

### Port already in use
**Solution**: Run on different port:
```bash
python manage.py runserver 8001
```

## Django Admin Access

1. Start server: `python manage.py runserver`
2. Go to: `http://localhost:8000/admin/`
3. Login with superuser credentials
4. Manage:
   - Users and profiles
   - Communities
   - Chat rooms and messages
   - Mentorship requests
   - Onboarding progress

## Frontend Integration Checklist

- [ ] Update API base URL in frontend (`http://localhost:8000`)
- [ ] Configure JWT token storage (localStorage/sessionStorage)
- [ ] Add auth header to API requests: `Authorization: Bearer <token>`
- [ ] Handle token refresh when needed
- [ ] Set up error handling for API responses
- [ ] Configure image upload endpoints
- [ ] Test all endpoints with frontend

## Database Models Diagram

```
User (Django built-in)
├── StudentProfile (1:1)
├── Community (M:M as creator)
│   └── Community (M:M as member)
├── ChatRoom (M:M as member)
│   └── Message (1:M)
├── MentorshipRequest (1:M as student/mentor)
│   └── Mentorship (1:1)
└── OnboardingStep (1:1)
```

## Security Notes

1. Keep `SECRET_KEY` confidential (already configured)
2. Never commit `.env` files with secrets
3. Use HTTPS in production
4. Change `DEBUG = False` in production
5. Configure allowed hosts properly
6. Use strong password requirements
7. Implement rate limiting for API
8. Validate all user inputs

## Production Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Generate new SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up proper database (PostgreSQL/MySQL)
- [ ] Configure email backend for notifications
- [ ] Set up HTTPS/SSL
- [ ] Configure static files serving (WhiteNoise/CDN)
- [ ] Set up error logging
- [ ] Configure backup strategy
- [ ] Use environment variables for sensitive data

## Support & Debugging

### Enable Debug Logging
Add to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Django Shell for Testing
```bash
python manage.py shell

# In shell:
from accounts.models import StudentProfile
StudentProfile.objects.all()
```

## Quick Commands Reference

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --fake-initial

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver

# Django shell
python manage.py shell

# Collect static files (production)
python manage.py collectstatic

# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json

# Clear cache
python manage.py clear_cache
```

---

**Now your backend is fully configured and connected to your frontend!**

Start the development server and begin integrating the frontend with the API endpoints.
