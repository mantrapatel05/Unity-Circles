# Unity Circles

A modern Django-based social platform for connecting students, facilitating mentorship, enabling real-time communication, and building vibrant communities.

## Features

### 💬 Real-time Chat System
- Create and manage chat rooms
- Send and receive messages instantly with 3-second polling
- Member management and chat room creation
- Responsive chat interface with modal support

### 📅 Meeting Scheduler
- Schedule and manage meetings
- Date and time picker for easy scheduling
- Attendee selection and management
- Join/leave meeting functionality
- Meeting duration tracking
- Zoom integration support

### 🏘️ Reddit-like Communities
- Create and browse communities
- Post content with upvote/downvote system
- Nested comments on posts
- Member management (join/leave communities)
- Community-specific feeds

### 👥 Mentorship System
- Connect mentors with mentees
- Mentorship request management
- Track mentorship relationships

### 🔐 Authentication
- User registration and login
- JWT token-based authentication
- Secure profile management

### 📱 Responsive Design
- Mobile-friendly interface
- Smooth animations and transitions
- Lucide icon integration

## Tech Stack

**Backend:**
- Django 4.2.28
- Django REST Framework
- SQLite Database
- Python 3.12.2

**Frontend:**
- HTML5
- CSS3 with custom animations
- Vanilla JavaScript (Fetch API)
- Lucide Icons

**Deployment Ready:**
- WSGI configuration
- Static files management
- Media file handling

## Project Structure

```
unity-circles/
├── accounts/          # User authentication and profiles
├── chat/              # Real-time messaging
├── core/              # Communities, posts, meetings
├── mentorship/        # Mentorship features
├── onboarding/        # User onboarding flow
├── templates/         # HTML templates
├── static/            # CSS and JavaScript files
├── media/             # User uploaded content
├── unity_circles/     # Project settings
└── manage.py          # Django management
```

## Installation

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mantrapatel05/Unity-Circles.git
   cd Unity-Circles
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

   Server will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user

### Chat
- `GET /api/chat/rooms/` - List all chat rooms
- `POST /api/chat/rooms/` - Create new chat room
- `GET /api/chat/rooms/{id}/` - Get room details
- `POST /api/chat/rooms/{id}/messages/` - Send message
- `GET /api/chat/rooms/{id}/messages/` - Get room messages

### Communities
- `GET /api/communities/` - List all communities
- `POST /api/communities/` - Create community
- `GET /api/communities/{id}/` - Get community details
- `POST /api/communities/{id}/join/` - Join community
- `POST /api/communities/{id}/leave/` - Leave community

### Posts
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `POST /api/posts/{id}/upvote/` - Upvote post
- `POST /api/posts/{id}/downvote/` - Downvote post

### Comments
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create comment
- `POST /api/comments/{id}/upvote/` - Upvote comment
- `POST /api/comments/{id}/downvote/` - Downvote comment

### Meetings
- `GET /api/meetings/` - List meetings
- `POST /api/meetings/` - Create meeting
- `POST /api/meetings/{id}/join/` - Join meeting
- `POST /api/meetings/{id}/leave/` - Leave meeting

### Users
- `GET /api/users/` - List users

## Key Features Breakdown

### Real-time Messaging
- Messages update every 3 seconds
- Chat room member management
- Create new chat rooms with selected members
- Clean, intuitive chat interface

### Smart Meeting Scheduler
- Calendar-style date picker
- Duration configuration
- Automatic attendee selection
- Status tracking (scheduled, completed, cancelled)

### Community Platform
- Hierarchical structure (communities → posts → comments)
- Voting system for content ranking
- Member counts and activity tracking
- Community-specific feeds

## Admin Panel

Access the Django admin panel at `/admin/` with superuser credentials to:
- Manage users, communities, posts, and meetings
- Moderate content
- View system statistics
- Manage user accounts

## Authentication Details

- JWT tokens stored in localStorage
- Token-based API authentication
- Secure login/logout flow
- Session management

## Database Models

### Core Models
- **StudentProfile** - User profile with role and interests
- **ChatRoom** - Group chat spaces
- **Message** - Chat messages
- **Community** - Discussion communities
- **Post** - Content in communities
- **PostComment** - Comments on posts
- **Meeting** - Scheduled meetings
- **MentorshipRequest** - Mentorship requests
- **Mentorship** - Active mentorships
- **OnboardingStep** - User onboarding progress

## Development Workflow

### Making Changes
```bash
# Create/modify models
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Testing API
- Use Postman or similar tool
- All endpoints require JWT authentication (except register/login)
- Include: `Authorization: Bearer {token}` in request headers

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- WebSocket integration for real-time messaging
- Video call support
- Notification system
- Advanced search functionality
- User recommendations
- Analytics dashboard
- Mobile app

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on the GitHub repository.

---

**Built with ❤️ using Django and modern web technologies**

**Repository:** https://github.com/mantrapatel05/Unity-Circles
