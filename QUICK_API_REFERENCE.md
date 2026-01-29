# Quick API Reference

## Base URL
```
http://localhost:8000
```

## Authentication Flow

### 1. Register
```
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 2. Login (Get Token)
```
POST /api/auth/token/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepass123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Use Token
```
Authorization: Bearer <access_token>
```

## User Management

### Get Current User
```
GET /api/auth/me/
Authorization: Bearer <token>
```

### Get User Profile
```
GET /api/auth/profile/
Authorization: Bearer <token>
```

### Update User Profile
```
PUT /api/auth/profile/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "phone_number": "+1234567890",
  "qualification": "BS Computer Science",
  "interests": "Web Development, AI",
  "role": "mentor",
  "bio": "Experienced developer with 5 years experience"
}
```

## Communities

### List Communities
```
GET /api/communities/
Authorization: Bearer <token>
```

### Create Community
```
POST /api/communities/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Python Developers",
  "description": "Community for Python enthusiasts",
  "category": "tech"
}
```

### Get Community Details
```
GET /api/communities/{id}/
Authorization: Bearer <token>
```

### Update Community
```
PUT /api/communities/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Advanced Python Developers",
  "description": "Updated description",
  "category": "tech"
}
```

### Delete Community
```
DELETE /api/communities/{id}/
Authorization: Bearer <token>
```

## Chat

### List Chat Rooms
```
GET /api/chat/rooms/
Authorization: Bearer <token>
```

### Create Chat Room
```
POST /api/chat/rooms/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "General Discussion",
  "description": "Room for general topics",
  "members": [1, 2, 3]
}
```

### Get Room Details
```
GET /api/chat/rooms/{id}/
Authorization: Bearer <token>
```

### Send Message
```
POST /api/chat/messages/
Authorization: Bearer <token>
Content-Type: application/json

{
  "room": 1,
  "content": "Hello everyone!"
}
```

### Get Messages
```
GET /api/chat/messages/
Authorization: Bearer <token>
```

## Mentorship

### List Mentorship Requests
```
GET /api/mentorship/requests/
Authorization: Bearer <token>
```

### Create Mentorship Request
```
POST /api/mentorship/requests/
Authorization: Bearer <token>
Content-Type: application/json

{
  "mentor": 2,
  "subject": "Learn Web Development",
  "description": "I want to learn full-stack web development"
}
```

### Accept Mentorship Request
```
POST /api/mentorship/requests/{id}/accept/
Authorization: Bearer <token>
```

### Reject Mentorship Request
```
POST /api/mentorship/requests/{id}/reject/
Authorization: Bearer <token>
```

### Get Active Mentorships
```
GET /api/mentorship/mentorships/
Authorization: Bearer <token>
```

### Update Mentorship Progress
```
PUT /api/mentorship/mentorships/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "goals": "Complete 3 projects",
  "progress": "Completed project 1"
}
```

## Onboarding

### Get Onboarding Progress
```
GET /api/onboarding/steps/
Authorization: Bearer <token>
```

### Complete Profile Step
```
POST /api/onboarding/steps/{id}/complete_profile/
Authorization: Bearer <token>
```

### Complete Interests Step
```
POST /api/onboarding/steps/{id}/complete_interests/
Authorization: Bearer <token>
```

### Complete Goals Step
```
POST /api/onboarding/steps/{id}/complete_goals/
Authorization: Bearer <token>
```

### Complete Community Step
```
POST /api/onboarding/steps/{id}/complete_community/
Authorization: Bearer <token>
```

## Status Codes

```
200 - OK (successful GET/PUT)
201 - Created (successful POST)
204 - No Content (successful DELETE)
400 - Bad Request (invalid data)
401 - Unauthorized (missing/invalid token)
403 - Forbidden (no permission)
404 - Not Found (resource doesn't exist)
500 - Server Error
```

## Error Response Example

```json
{
  "detail": "Authentication credentials were not provided."
}
```

## Token Refresh

When access token expires:
```
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}

Response:
{
  "access": "new_access_token"
}
```

## Pagination

Responses support pagination:
```
GET /api/communities/?page=1&page_size=10
Authorization: Bearer <token>
```

## Filtering & Search

```
GET /api/communities/?category=tech
GET /api/chat/rooms/?search=general
```

## Tips

1. Always include `Authorization: Bearer <token>` header for protected endpoints
2. Use `Content-Type: application/json` for POST/PUT requests
3. Keep tokens secure and never expose them
4. Refresh tokens when access tokens expire
5. Test endpoints with Postman or Insomnia first
