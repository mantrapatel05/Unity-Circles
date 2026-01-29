# All API Endpoints - Complete Reference

## Base URL
```
http://localhost:8000
```

## Authentication Endpoints

### 1. Register New User
```
POST /api/auth/register/
Content-Type: application/json

REQUEST:
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}

RESPONSE (201):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 2. Login - Get JWT Token
```
POST /api/auth/token/
Content-Type: application/json

REQUEST:
{
  "username": "john_doe",
  "password": "securepass123"
}

RESPONSE (200):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Refresh Access Token
```
POST /api/auth/token/refresh/
Content-Type: application/json
Authorization: Bearer <refresh_token>

REQUEST:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

RESPONSE (200):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. Get Current User Info
```
GET /api/auth/me/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 5. Get User Profile
```
GET /api/auth/profile/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "phone_number": "+1234567890",
  "qualification": "BS Computer Science",
  "interests": "Web Development, AI",
  "role": "student",
  "bio": "Passionate about learning",
  "profile_picture": null,
  "created_at": "2024-01-29T10:00:00Z"
}
```

### 6. Create/Update User Profile
```
POST /api/auth/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "phone_number": "+1234567890",
  "qualification": "BS Computer Science",
  "interests": "Web Development, AI",
  "role": "student",
  "bio": "Passionate about learning"
}

RESPONSE (201):
{
  "id": 1,
  "user": {...},
  "phone_number": "+1234567890",
  ...
}
```

### 7. Update User Profile (by ID)
```
PUT /api/auth/profile/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "phone_number": "+1234567890",
  "role": "mentor",
  ...
}

RESPONSE (200):
{
  "id": 1,
  ...updated data...
}
```

---

## Community Endpoints

### 1. List All Communities
```
GET /api/communities/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Python Developers",
      "description": "Community for Python developers",
      "category": "tech",
      "members": [...],
      "creator": {...},
      "created_at": "2024-01-29T10:00:00Z"
    },
    ...
  ]
}
```

### 2. Create New Community
```
POST /api/communities/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "name": "Python Developers",
  "description": "Community for Python developers",
  "category": "tech"
}

RESPONSE (201):
{
  "id": 1,
  "name": "Python Developers",
  "description": "Community for Python developers",
  "category": "tech",
  "members": [],
  "creator": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2024-01-29T10:00:00Z"
}
```

### 3. Get Community Details
```
GET /api/communities/{id}/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "id": 1,
  "name": "Python Developers",
  "description": "Community for Python developers",
  "category": "tech",
  "members": [
    {
      "id": 1,
      "username": "john_doe"
    },
    ...
  ],
  "creator": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2024-01-29T10:00:00Z",
  "updated_at": "2024-01-29T11:00:00Z"
}
```

### 4. Update Community
```
PUT /api/communities/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "name": "Advanced Python Developers",
  "description": "For advanced Python developers"
}

RESPONSE (200):
{
  "id": 1,
  ...updated data...
}
```

### 5. Delete Community
```
DELETE /api/communities/{id}/
Authorization: Bearer <access_token>

RESPONSE (204): No Content
```

---

## Chat Endpoints

### 1. List Chat Rooms
```
GET /api/chat/rooms/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "General Discussion",
      "description": "General chat",
      "members": [...],
      "messages": [...],
      "created_at": "2024-01-29T10:00:00Z"
    },
    ...
  ]
}
```

### 2. Create Chat Room
```
POST /api/chat/rooms/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "name": "General Discussion",
  "description": "General chat room",
  "members": [1, 2, 3]
}

RESPONSE (201):
{
  "id": 1,
  "name": "General Discussion",
  "description": "General chat room",
  "members": [
    {"id": 1, "username": "john_doe"},
    {"id": 2, "username": "jane_smith"},
    {"id": 3, "username": "bob_wilson"}
  ],
  "messages": [],
  "created_at": "2024-01-29T10:00:00Z"
}
```

### 3. Get Room Details
```
GET /api/chat/rooms/{id}/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "id": 1,
  "name": "General Discussion",
  "messages": [
    {
      "id": 1,
      "sender": {
        "id": 1,
        "username": "john_doe"
      },
      "content": "Hello everyone!",
      "created_at": "2024-01-29T10:05:00Z"
    },
    ...
  ],
  "created_at": "2024-01-29T10:00:00Z"
}
```

### 4. Send Message
```
POST /api/chat/messages/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "room": 1,
  "content": "Hello everyone!"
}

RESPONSE (201):
{
  "id": 1,
  "room": 1,
  "sender": {
    "id": 1,
    "username": "john_doe"
  },
  "content": "Hello everyone!",
  "created_at": "2024-01-29T10:05:00Z"
}
```

### 5. Get All Messages
```
GET /api/chat/messages/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "room": 1,
      "sender": {...},
      "content": "Hello!",
      "created_at": "2024-01-29T10:05:00Z"
    },
    ...
  ]
}
```

---

## Mentorship Endpoints

### 1. List Mentorship Requests
```
GET /api/mentorship/requests/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "student": {
        "id": 1,
        "username": "john_doe"
      },
      "mentor": {
        "id": 2,
        "username": "jane_smith"
      },
      "subject": "Learn Web Development",
      "description": "I want to learn full-stack web development",
      "status": "pending",
      "created_at": "2024-01-29T10:00:00Z"
    },
    ...
  ]
}
```

### 2. Create Mentorship Request
```
POST /api/mentorship/requests/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "mentor": 2,
  "subject": "Learn Web Development",
  "description": "I want to learn full-stack web development"
}

RESPONSE (201):
{
  "id": 1,
  "student": {
    "id": 1,
    "username": "john_doe"
  },
  "mentor": {
    "id": 2,
    "username": "jane_smith"
  },
  "subject": "Learn Web Development",
  "description": "I want to learn full-stack web development",
  "status": "pending",
  "created_at": "2024-01-29T10:00:00Z"
}
```

### 3. Accept Mentorship Request
```
POST /api/mentorship/requests/{id}/accept/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "status": "Mentorship accepted"
}
```

### 4. Reject Mentorship Request
```
POST /api/mentorship/requests/{id}/reject/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "status": "Mentorship rejected"
}
```

### 5. List Active Mentorships
```
GET /api/mentorship/mentorships/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "request": {
        "id": 1,
        "student": {...},
        "mentor": {...},
        "subject": "Learn Web Development",
        "status": "accepted"
      },
      "start_date": "2024-01-29T10:00:00Z",
      "end_date": null,
      "goals": "Complete 3 projects",
      "progress": "Project 1 completed"
    },
    ...
  ]
}
```

### 6. Update Mentorship
```
PUT /api/mentorship/mentorships/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

REQUEST:
{
  "goals": "Complete 3 projects",
  "progress": "Project 1 completed"
}

RESPONSE (200):
{
  "id": 1,
  ...updated data...
}
```

---

## Onboarding Endpoints

### 1. Get Onboarding Progress
```
GET /api/onboarding/steps/
Authorization: Bearer <access_token>

RESPONSE (200):
[
  {
    "id": 1,
    "user": 1,
    "profile_completed": true,
    "interests_completed": true,
    "goals_completed": false,
    "community_completed": false,
    "is_completed": false,
    "created_at": "2024-01-29T10:00:00Z",
    "updated_at": "2024-01-29T11:00:00Z"
  }
]
```

### 2. Complete Profile Step
```
POST /api/onboarding/steps/{id}/complete_profile/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "status": "Profile step completed"
}
```

### 3. Complete Interests Step
```
POST /api/onboarding/steps/{id}/complete_interests/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "status": "Interests step completed"
}
```

### 4. Complete Goals Step
```
POST /api/onboarding/steps/{id}/complete_goals/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "status": "Goals step completed"
}
```

### 5. Complete Community Step
```
POST /api/onboarding/steps/{id}/complete_community/
Authorization: Bearer <access_token>

RESPONSE (200):
{
  "status": "Community step completed"
}
```

---

## Common Response Codes

```
200 OK              - Successful GET/PUT
201 Created         - Successful POST
204 No Content      - Successful DELETE
400 Bad Request     - Invalid data
401 Unauthorized    - Missing/invalid token
403 Forbidden       - No permission
404 Not Found       - Resource doesn't exist
500 Server Error    - Internal server error
```

---

## Error Response Example

```json
{
  "detail": "Authentication credentials were not provided."
}
```

or

```json
{
  "field_name": [
    "This field is required."
  ]
}
```

---

## Authentication Header Template

All authenticated endpoints require:
```
Authorization: Bearer <access_token>
```

Replace `<access_token>` with the token received from `/api/auth/token/`

---

## Testing Tips

1. Use Postman for testing API
2. Store tokens in environment variables
3. Set Authorization header globally in Postman
4. Test each endpoint systematically
5. Keep this file handy for reference

---

**All 30+ endpoints are ready for integration!**
