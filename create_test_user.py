#!/usr/bin/env python
"""
Create a test user for Unity Circles
Run this script: python create_test_user.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unity_circles.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StudentProfile

def create_test_user():
    """Create a test user with profile"""
    
    # Check if user already exists
    if User.objects.filter(username='testuser').exists():
        print("❌ Test user 'testuser' already exists!")
        print("   You can delete it in Django admin or use a different username.")
        return False
    
    try:
        # Create user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create student profile
        profile = StudentProfile.objects.create(
            user=user,
            bio='Test user for Unity Circles',
            role='student',
            interests='Testing, Development'
        )
        
        print("✅ Test user created successfully!")
        print("")
        print("Login credentials:")
        print("  Username: testuser")
        print("  Password: testpass123")
        print("")
        print("You can now login at: http://127.0.0.1:8000/login/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Unity Circles - Test User Creator")
    print("=" * 50)
    print("")
    create_test_user()
    print("")
    print("=" * 50)
