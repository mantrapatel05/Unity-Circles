# Frontend Integration Guide

This document explains how to connect your frontend (HTML/JS) to the backend API.

## Overview

Your backend now exposes RESTful API endpoints that your frontend can consume. All data is exchanged in JSON format.

## Base Setup in JavaScript

### 1. Set API Base URL

Create a config file or add to your main.js:

```javascript
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINTS = {
  AUTH: `${API_BASE_URL}/api/auth`,
  COMMUNITIES: `${API_BASE_URL}/api/communities`,
  CHAT: `${API_BASE_URL}/api/chat`,
  MENTORSHIP: `${API_BASE_URL}/api/mentorship`,
  ONBOARDING: `${API_BASE_URL}/api/onboarding`,
};
```

### 2. Store JWT Token

After login, store the token:

```javascript
// Save token
localStorage.setItem('access_token', response.data.access);
localStorage.setItem('refresh_token', response.data.refresh);

// Retrieve token
const token = localStorage.getItem('access_token');
```

### 3. Helper Function for API Calls

```javascript
async function apiCall(endpoint, method = 'GET', data = null) {
  const token = localStorage.getItem('access_token');
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  // Add auth token if it exists
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`;
  }
  
  // Add body for POST/PUT
  if (data) {
    options.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(endpoint, options);
    
    if (response.status === 401) {
      // Token expired, refresh it
      await refreshToken();
      return apiCall(endpoint, method, data); // Retry
    }
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Call Failed:', error);
    throw error;
  }
}
```

## Page-by-Page Integration

### 1. Landing Page (landing.html)

No API integration needed - static page that links to signup/login.

**Links to add:**
- Sign Up: `/signup/`
- Log In: `/api/auth/token/`
- Communities: `/communities/`

### 2. Sign Up Page (signup.html)

```javascript
async function handleSignup(e) {
  e.preventDefault();
  
  const formData = {
    username: document.getElementById('username').value,
    email: document.getElementById('email').value,
    password: document.getElementById('password').value,
    first_name: document.getElementById('first_name').value,
    last_name: document.getElementById('last_name').value,
  };
  
  try {
    const response = await apiCall(
      `${API_ENDPOINTS.AUTH}/register/`,
      'POST',
      formData
    );
    
    // Redirect to login
    window.location.href = '/login/';
  } catch (error) {
    alert('Signup failed: ' + error.message);
  }
}
```

**Form Fields:**
- username
- email
- password
- first_name
- last_name

### 3. Login Page (login.html)

```javascript
async function handleLogin(e) {
  e.preventDefault();
  
  const credentials = {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value,
  };
  
  try {
    const response = await apiCall(
      `${API_ENDPOINTS.AUTH}/token/`,
      'POST',
      credentials
    );
    
    localStorage.setItem('access_token', response.access);
    localStorage.setItem('refresh_token', response.refresh);
    
    // Redirect to dashboard
    window.location.href = '/dashboard/';
  } catch (error) {
    alert('Login failed: ' + error.message);
  }
}
```

### 4. Dashboard (dashboard.html)

Display user info and latest communities:

```javascript
async function loadDashboard() {
  try {
    // Get current user
    const userResponse = await apiCall(`${API_ENDPOINTS.AUTH}/me/`);
    document.getElementById('user-name').textContent = userResponse.username;
    
    // Get communities
    const communitiesResponse = await apiCall(
      `${API_ENDPOINTS.COMMUNITIES}/`
    );
    displayCommunities(communitiesResponse.results || communitiesResponse);
  } catch (error) {
    console.error('Failed to load dashboard:', error);
  }
}

function displayCommunities(communities) {
  const container = document.getElementById('communities-list');
  container.innerHTML = communities.map(community => `
    <div class="community-card">
      <h3>${community.name}</h3>
      <p>${community.description}</p>
      <span class="badge">${community.category}</span>
      <button onclick="joinCommunity(${community.id})">Join</button>
    </div>
  `).join('');
}
```

### 5. Profile Page (profile.html)

```javascript
async function loadProfile() {
  try {
    const response = await apiCall(`${API_ENDPOINTS.AUTH}/profile/`);
    
    // Populate form
    document.getElementById('phone').value = response.phone_number || '';
    document.getElementById('qualification').value = response.qualification || '';
    document.getElementById('interests').value = response.interests || '';
    document.getElementById('role').value = response.role || 'student';
    document.getElementById('bio').value = response.bio || '';
  } catch (error) {
    console.error('Failed to load profile:', error);
  }
}

async function updateProfile(e) {
  e.preventDefault();
  
  const profileData = {
    phone_number: document.getElementById('phone').value,
    qualification: document.getElementById('qualification').value,
    interests: document.getElementById('interests').value,
    role: document.getElementById('role').value,
    bio: document.getElementById('bio').value,
  };
  
  try {
    const response = await apiCall(
      `${API_ENDPOINTS.AUTH}/profile/1/`, // Replace 1 with actual profile ID
      'PUT',
      profileData
    );
    alert('Profile updated successfully!');
  } catch (error) {
    alert('Failed to update profile: ' + error.message);
  }
}
```

### 6. Communities Page (communities.html)

```javascript
async function loadCommunities() {
  try {
    const response = await apiCall(`${API_ENDPOINTS.COMMUNITIES}/`);
    displayCommunities(response.results || response);
  } catch (error) {
    console.error('Failed to load communities:', error);
  }
}

async function createCommunity(e) {
  e.preventDefault();
  
  const communityData = {
    name: document.getElementById('community-name').value,
    description: document.getElementById('community-desc').value,
    category: document.getElementById('community-category').value,
  };
  
  try {
    await apiCall(
      `${API_ENDPOINTS.COMMUNITIES}/`,
      'POST',
      communityData
    );
    alert('Community created!');
    loadCommunities();
  } catch (error) {
    alert('Failed to create community: ' + error.message);
  }
}
```

### 7. Mentors Page (mentors.html)

```javascript
async function loadMentorshipRequests() {
  try {
    const response = await apiCall(`${API_ENDPOINTS.MENTORSHIP}/requests/`);
    displayRequests(response.results || response);
  } catch (error) {
    console.error('Failed to load mentorship requests:', error);
  }
}

async function createMentorshipRequest(e) {
  e.preventDefault();
  
  const requestData = {
    mentor: document.getElementById('mentor-id').value,
    subject: document.getElementById('subject').value,
    description: document.getElementById('description').value,
  };
  
  try {
    await apiCall(
      `${API_ENDPOINTS.MENTORSHIP}/requests/`,
      'POST',
      requestData
    );
    alert('Mentorship request sent!');
    loadMentorshipRequests();
  } catch (error) {
    alert('Failed to send request: ' + error.message);
  }
}

async function acceptMentorship(requestId) {
  try {
    await apiCall(
      `${API_ENDPOINTS.MENTORSHIP}/requests/${requestId}/accept/`,
      'POST'
    );
    alert('Mentorship accepted!');
    loadMentorshipRequests();
  } catch (error) {
    alert('Failed to accept: ' + error.message);
  }
}
```

### 8. Messages Page (messages.html)

```javascript
async function loadChatRooms() {
  try {
    const response = await apiCall(`${API_ENDPOINTS.CHAT}/rooms/`);
    displayChatRooms(response.results || response);
  } catch (error) {
    console.error('Failed to load chat rooms:', error);
  }
}

async function sendMessage(roomId, e) {
  e.preventDefault();
  
  const messageData = {
    room: roomId,
    content: document.getElementById('message-input').value,
  };
  
  try {
    await apiCall(
      `${API_ENDPOINTS.CHAT}/messages/`,
      'POST',
      messageData
    );
    document.getElementById('message-input').value = '';
    loadMessages(roomId);
  } catch (error) {
    alert('Failed to send message: ' + error.message);
  }
}

async function loadMessages(roomId) {
  try {
    const response = await apiCall(`${API_ENDPOINTS.CHAT}/messages/`);
    const messages = response.filter(msg => msg.room === roomId);
    displayMessages(messages);
  } catch (error) {
    console.error('Failed to load messages:', error);
  }
}
```

### 9. Onboarding Page (onboarding.html)

```javascript
async function loadOnboardingProgress() {
  try {
    const response = await apiCall(`${API_ENDPOINTS.ONBOARDING}/steps/`);
    const step = response[0]; // Get first result
    
    updateOnboardingUI(step);
  } catch (error) {
    console.error('Failed to load onboarding:', error);
  }
}

async function completeOnboardingStep(stepId, stepType) {
  try {
    await apiCall(
      `${API_ENDPOINTS.ONBOARDING}/steps/${stepId}/complete_${stepType}/`,
      'POST'
    );
    alert('Step completed!');
    loadOnboardingProgress();
  } catch (error) {
    alert('Failed to complete step: ' + error.message);
  }
}

function updateOnboardingUI(step) {
  const progress = [
    { name: 'Profile', completed: step.profile_completed },
    { name: 'Interests', completed: step.interests_completed },
    { name: 'Goals', completed: step.goals_completed },
    { name: 'Community', completed: step.community_completed },
  ];
  
  const progressBar = document.getElementById('progress');
  const completedCount = progress.filter(p => p.completed).length;
  const percentage = (completedCount / progress.length) * 100;
  
  progressBar.style.width = percentage + '%';
}
```

## Handling Authentication

### Check if User is Logged In

```javascript
function isLoggedIn() {
  return !!localStorage.getItem('access_token');
}

// Protect pages
if (!isLoggedIn() && !isPublicPage()) {
  window.location.href = '/login/';
}
```

### Logout

```javascript
function handleLogout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/landing/';
}
```

### Refresh Token

```javascript
async function refreshToken() {
  const refresh = localStorage.getItem('refresh_token');
  
  try {
    const response = await fetch(`${API_ENDPOINTS.AUTH}/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    });
    
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
  } catch (error) {
    console.error('Token refresh failed:', error);
    handleLogout(); // Redirect to login
  }
}
```

## Error Handling

```javascript
function handleApiError(error) {
  if (error.status === 401) {
    // Unauthorized - clear tokens and redirect to login
    localStorage.clear();
    window.location.href = '/login/';
  } else if (error.status === 403) {
    alert('You do not have permission to perform this action');
  } else if (error.status === 404) {
    alert('Resource not found');
  } else if (error.status === 400) {
    alert('Invalid request data');
  } else {
    alert('An error occurred: ' + error.message);
  }
}
```

## CORS Note

The backend is configured to accept requests from:
- `http://localhost:3000` (if frontend runs on port 3000)
- `http://127.0.0.1:3000`

If your frontend is on a different port/domain, update `CORS_ALLOWED_ORIGINS` in `unity_circles/settings.py`.

## Testing with Postman

1. Download Postman
2. Import the API endpoints
3. Set `{{base_url}}` = `http://localhost:8000`
4. Create requests for each endpoint
5. Save tokens and use in headers for authenticated requests

## Next Steps

1. Initialize all event listeners when pages load
2. Add form validation
3. Implement loading spinners
4. Add error toasts/notifications
5. Set up automatic token refresh
6. Implement real-time chat with WebSockets (optional)
