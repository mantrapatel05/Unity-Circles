#!/usr/bin/env python
"""
Quick Fix Script for Meetings Not Working
This script will:
1. Check if the database is migrated
2. Verify the Meeting model exists
3. Check for users
4. Create test meetings if none exist
5. Test the API endpoint
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unity_circles.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Meeting
from datetime import datetime, timedelta
from django.utils import timezone

print("=" * 70)
print("MEETINGS QUICK FIX TOOL")
print("=" * 70)

# Step 1: Check database
print("\n[1] Checking database...")
try:
    meeting_count = Meeting.objects.count()
    print(f"✓ Database accessible")
    print(f"  - Found {meeting_count} meetings")
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("\n🔧 FIX: Run the following commands:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    sys.exit(1)

# Step 2: Check for users
print("\n[2] Checking for users...")
user_count = User.objects.count()
if user_count == 0:
    print(f"✗ No users found")
    print("\n🔧 FIX: Create a user:")
    print("   python manage.py createsuperuser")
    sys.exit(1)
else:
    print(f"✓ Found {user_count} users")
    sample_users = User.objects.all()[:3]
    for u in sample_users:
        print(f"  - {u.username} ({u.email})")

# Step 3: Check for meetings
print("\n[3] Checking for meetings...")
if meeting_count == 0:
    print("⚠️  No meetings found")
    
    # Offer to create test meetings
    user_input = input("\nWould you like to create test meetings? (y/n): ")
    if user_input.lower() == 'y':
        print("\n[4] Creating test meetings...")
        mentor = User.objects.first()
        
        # Create 3 test meetings
        test_meetings = [
            {
                'title': 'Career Development Discussion',
                'description': 'Let\'s discuss your career path and goals for the next 6 months.',
                'scheduled_time': timezone.now() + timedelta(days=2),
                'duration_minutes': 60,
                'status': 'scheduled',
                'zoom_link': 'https://zoom.us/j/123456789'
            },
            {
                'title': 'Technical Skills Workshop',
                'description': 'Hands-on workshop covering Python best practices and design patterns.',
                'scheduled_time': timezone.now() + timedelta(days=5),
                'duration_minutes': 90,
                'status': 'scheduled',
                'zoom_link': 'https://meet.google.com/abc-defg-hij'
            },
            {
                'title': 'Code Review Session',
                'description': 'Review your recent project and provide feedback on architecture.',
                'scheduled_time': timezone.now() + timedelta(days=7),
                'duration_minutes': 45,
                'status': 'scheduled',
            }
        ]
        
        created_count = 0
        for meeting_data in test_meetings:
            meeting = Meeting.objects.create(mentor=mentor, **meeting_data)
            print(f"  ✓ Created: {meeting.title}")
            created_count += 1
        
        print(f"\n✓ Successfully created {created_count} test meetings")
        meeting_count = Meeting.objects.count()
    else:
        print("  Skipping test meeting creation")
else:
    print(f"✓ Found {meeting_count} meetings")
    print("\nRecent meetings:")
    for m in Meeting.objects.all()[:5]:
        print(f"  - {m.title}")
        print(f"    Mentor: {m.mentor.username}")
        print(f"    Date: {m.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"    Status: {m.status}")

# Step 4: Test API endpoint
print("\n[5] Testing API endpoint...")
from rest_framework.test import APIClient

client = APIClient()

# Test without auth
response = client.get('/api/meetings/')
print(f"  - GET /api/meetings/ (no auth): {response.status_code}")

# Test with auth
user = User.objects.first()
client.force_authenticate(user=user)
response = client.get('/api/meetings/')
print(f"  - GET /api/meetings/ (with auth): {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"  ✓ API working! Returned {len(data)} meetings")
    
    # Show sample response
    if len(data) > 0:
        sample = data[0]
        print(f"\n  Sample meeting data:")
        print(f"    Title: {sample.get('title')}")
        print(f"    Mentor: {sample.get('mentor', {}).get('username')}")
        print(f"    Attendees: {sample.get('attendees_count', 0)}")
else:
    print(f"  ✗ API error: {response.status_code}")
    try:
        print(f"    {response.json()}")
    except:
        print(f"    {response.content}")

# Step 5: Check template
print("\n[6] Checking templates...")
template_path = os.path.join(os.path.dirname(__file__), 'templates', 'meetings.html')
if os.path.exists(template_path):
    print(f"  ✓ meetings.html found")
    size = os.path.getsize(template_path)
    print(f"    Size: {size} bytes")
else:
    print(f"  ✗ meetings.html NOT FOUND")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

all_good = True

if user_count == 0:
    print("✗ No users - create a superuser")
    all_good = False
else:
    print(f"✓ {user_count} users exist")

if meeting_count == 0:
    print("⚠️  No meetings - create some test meetings")
    all_good = False
else:
    print(f"✓ {meeting_count} meetings exist")

if response.status_code == 200:
    print("✓ API endpoint working")
else:
    print("✗ API endpoint has issues")
    all_good = False

if os.path.exists(template_path):
    print("✓ Template exists")
else:
    print("✗ Template missing")
    all_good = False

print("\n" + "=" * 70)
if all_good and meeting_count > 0:
    print("🎉 EVERYTHING LOOKS GOOD!")
    print("\nNext steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Log in to your account")
    print("3. Visit: http://127.0.0.1:8000/meetings/")
    print("4. You should see your meetings!")
else:
    print("⚠️  ISSUES DETECTED")
    print("\nPlease address the issues above, then:")
    print("1. Run this script again")
    print("2. Or check MEETINGS_TROUBLESHOOTING.md for detailed help")

print("=" * 70)
