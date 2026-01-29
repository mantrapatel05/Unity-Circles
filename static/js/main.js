// static/js/main.js

async function login(username, password) {
    const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    
    const data = await response.json();
    
    if (response.ok) {
        // Save token
        localStorage.setItem('access_token', data.tokens.access);
        localStorage.setItem('refresh_token', data.tokens.refresh);
        console.log('Login successful!');
        // Redirect to dashboard
        window.location.href = '/dashboard';
    } else {
        console.error('Login failed:', data.error);
    }
}

async function findMentors() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://127.0.0.1:8000/api/mentorship/requests/find_mentors/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        }
    });
    
    const data = await response.json();
    
    // Display mentors
    displayMentors(data.recommendations);
}

function displayMentors(mentors) {
    const mentorList = document.getElementById('mentor-list');
    mentorList.innerHTML = '';
    
    mentors.forEach(mentor => {
        const mentorCard = `
            <div class="mentor-card">
                <h3>${mentor.mentor.user.username}</h3>
                <p>Year: ${mentor.mentor.year}</p>
                <p>Branch: ${mentor.mentor.branch}</p>
                <p>Compatibility: ${mentor.compatibility_score}%</p>
                <button onclick="sendRequest(${mentor.mentor.id})">Send Request</button>
            </div>
        `;
        mentorList.innerHTML += mentorCard;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    const menuBtn = document.getElementById('mobile-menu-toggle');
    const navLinks = document.getElementById('nav-links-container');

    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
});

