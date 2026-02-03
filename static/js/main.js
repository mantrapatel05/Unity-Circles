// static/js/main.js

// Smooth page transitions
document.addEventListener('DOMContentLoaded', () => {
    // Animate all cards on load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });

    // Smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lucide icons initialization
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Smooth hover effects
    const buttons = document.querySelectorAll('.btn, .nav-link, .dropdown-item');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // Mobile menu toggle with smooth animation
    const mobileMenuBtn = document.getElementById('mobile-menu-toggle');
    const navLinks = document.getElementById('nav-links-container');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navLinks.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    }
});

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
        
        // Smooth page transition
        document.body.style.transition = 'opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        document.body.style.opacity = '0';
        
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 400);
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

