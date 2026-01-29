# Unity Circles - Backend API Documentation

## Project Structure

```
unity_circles/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── accounts/              # User authentication and profile management
│   ├── models.py         # StudentProfile model
│   ├── views.py          # Authentication views
│   ├── serializers.py    # DRF serializers
│   ├── urls.py          # Auth endpoints
│   └── admin.py         # Admin configuration
├── core/                 # Communities management
│   ├── models.py        # Community model
│   ├── views.py         # Community viewset
│   ├── serializers.py   # Community serializers
│   ├── urls.py          # Community endpoints
│   └── admin.py         # Admin configuration
├── chat/                # Messaging system
│   ├── models.py        # ChatRoom and Message models
│   ├── views.py         # Chat viewsets
│   ├── serializers.py   # Chat serializers
│   ├── urls.py          # Chat endpoints
│   └── admin.py         # Admin configuration
├── mentorship/          # Mentorship features
│   ├── models.py        # MentorshipRequest and Mentorship models
│   ├── views.py         # Mentorship viewsets
│   ├── serializers.py   # Mentorship serializers
│   ├── urls.py          # Mentorship endpoints
│   └── admin.py         # Admin configuration
├── onboarding/          # User onboarding system
│   ├── models.py        # OnboardingStep model
│   ├── views.py         # Onboarding viewsets
│   ├── serializers.py   # Onboarding serializers
│   ├── urls.py          # Onboarding endpoints
│   └── admin.py         # Admin configuration
├── unity_circles/       # Project settings
│   ├── settings.py      # Django settings
│   ├── urls.py          # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS)
└── README.md           # This file
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication (`/api/auth/`)

#### User Registration
- **POST** `/api/auth/register/`
  - Create new user account
  - Required fields: `username`, `email`, `password`, `first_name`, `last_name`
  - Returns: User data with ID

#### Get Current User
- **GET** `/api/auth/me/`
  - Get logged-in user information
  - Requires: Authentication token

#### Token Endpoints
- **POST** `/api/auth/token/`
  - Obtain JWT token
  - Required fields: `username`, `password`
  - Returns: `access` and `refresh` tokens

- **POST** `/api/auth/token/refresh/`
  - Refresh access token
  - Required fields: `refresh` token

#### Student Profile
- **GET** `/api/auth/profile/`
  - Get current user's profile
- **POST** `/api/auth/profile/`
  - Create/update profile
- **PUT** `/api/auth/profile/{id}/`
  - Update profile details

### Communities (`/api/communities/`)
- **GET** `/api/communities/` - List all communities
- **POST** `/api/communities/` - Create new community
- **GET** `/api/communities/{id}/` - Get community details
- **PUT** `/api/communities/{id}/` - Update community
- **DELETE** `/api/communities/{id}/` - Delete community

### Chat (`/api/chat/`)

#### Chat Rooms
- **GET** `/api/chat/rooms/` - List user's chat rooms
- **POST** `/api/chat/rooms/` - Create new chat room
- **GET** `/api/chat/rooms/{id}/` - Get room details
- **PUT** `/api/chat/rooms/{id}/` - Update room

#### Messages
- **GET** `/api/chat/messages/` - List messages
- **POST** `/api/chat/messages/` - Send message
- **GET** `/api/chat/messages/{id}/` - Get message details

### Mentorship (`/api/mentorship/`)

#### Mentorship Requests
- **GET** `/api/mentorship/requests/` - List requests
- **POST** `/api/mentorship/requests/` - Create request
- **GET** `/api/mentorship/requests/{id}/` - Get request details
- **POST** `/api/mentorship/requests/{id}/accept/` - Accept mentorship
- **POST** `/api/mentorship/requests/{id}/reject/` - Reject mentorship

#### Mentorships
- **GET** `/api/mentorship/mentorships/` - List active mentorships
- **GET** `/api/mentorship/mentorships/{id}/` - Get mentorship details
- **PUT** `/api/mentorship/mentorships/{id}/` - Update mentorship

### Onboarding (`/api/onboarding/`)

#### Onboarding Steps
- **GET** `/api/onboarding/steps/` - Get onboarding progress
- **POST** `/api/onboarding/steps/{id}/complete_profile/` - Mark profile as complete
- **POST** `/api/onboarding/steps/{id}/complete_interests/` - Mark interests as complete
- **POST** `/api/onboarding/steps/{id}/complete_goals/` - Mark goals as complete
- **POST** `/api/onboarding/steps/{id}/complete_community/` - Mark community as complete

## Authentication

All API endpoints (except registration) require JWT token authentication.

### Getting a Token
```bash
POST /api/auth/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

### Using the Token
Include in request header:
```
Authorization: Bearer <your_access_token>
```

## Models Overview

### StudentProfile
- OneToOne relationship with User
- Fields: phone_number, qualification, interests, role, bio, profile_picture
- Roles: student, mentor, both

### Community
- name, description, category
- Many-to-many relationship with Users (members)
- Categories: tech, business, arts, science, health, other

### ChatRoom
- name, description
- Many-to-many relationship with Users (members)

### Message
- Foreign key to ChatRoom and User (sender)
- content, created_at

### MentorshipRequest
- Foreign keys to User (student, mentor)
- subject, description, status
- Status: pending, accepted, rejected, completed

### Mentorship
- OneToOne relationship with MentorshipRequest
- goals, progress, start_date, end_date

### OnboardingStep
- OneToOne relationship with User
- Tracks completion of: profile, interests, goals, community

## Frontend Integration

Frontend pages connect to backend through these main endpoints:

1. **landing.html** - No auth required, connects to `/` (landing page)
2. **signup.html** - Connects to `/api/auth/register/`
3. **dashboard.html** - Requires auth, connects to `/api/auth/me/` and community endpoints
4. **profile.html** - Connects to `/api/auth/profile/`
5. **communities.html** - Connects to `/api/communities/`
6. **mentors.html** - Connects to `/api/mentorship/requests/`
7. **messages.html** - Connects to `/api/chat/rooms/` and `/api/chat/messages/`
8. **meetings.html** - Connects to community and mentorship endpoints
9. **onboarding.html** - Connects to `/api/onboarding/steps/`

## CORS Configuration

The API accepts requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## Static Files

Static files are served from:
- CSS: `/static/css/`
- JavaScript: `/static/js/`
- Media uploads: `/media/`

## Admin Panel

Access Django admin at `/admin/` with superuser credentials.

Manage:
- User accounts
- Student profiles
- Communities
- Chat rooms and messages
- Mentorship requests and relationships
- Onboarding progress

## Common Issues & Solutions

### Issue: "No module named 'rest_framework'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "No module named 'corsheaders'"
**Solution**: Run `pip install django-cors-headers`

### Issue: "Migrations are not applied"
**Solution**: Run `python manage.py migrate`

### Issue: "Authentication failed"
**Solution**: Ensure you're sending JWT token in header: `Authorization: Bearer <token>`

## Development Tips

1. Use Django shell to test models:
   ```bash
   python manage.py shell
   ```

2. Access API documentation at `/api/` endpoints (DRF browsable API)

3. For testing, use tools like:
   - Postman
   - Insomnia
   - curl commands

4. Enable debug mode in settings.py for development:
   ```python
   DEBUG = True
   ```

## Next Steps

1. Configure frontend to use API endpoints
2. Set up WebSocket for real-time chat (optional)
3. Configure email for notifications
4. Set up image upload and storage
5. Deploy to production with proper security settings
