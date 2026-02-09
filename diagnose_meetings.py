#!/usr/bin/env python
"""
Meetings Diagnostic Script
Run this to check what's wrong with meetings
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
from django.urls import reverse, resolve
from rest_framework.test import APIClient

print("=" * 60)
print("MEETINGS DIAGNOSTIC")
print("=" * 60)

# Check if Meeting model exists
print("\n1. ✓ Meeting Model Check")
print(f"   Model: {Meeting}")
print(f"   Fields: {[f.name for f in Meeting._meta.get_fields()]}")

# Check if there are any meetings
print("\n2. Meeting Count")
count = Meeting.objects.count()
print(f"   Total meetings in database: {count}")

if count > 0:
    print(f"   Sample meeting: {Meeting.objects.first()}")

# Check if users exist
print("\n3. User Check")
user_count = User.objects.count()
print(f"   Total users: {user_count}")

# Check URL routing
print("\n4. URL Routing Check")
try:
    from core.urls import urlpatterns
    print(f"   Core URL patterns loaded: ✓")
    
    # Find API routes
    api_routes = [str(p.pattern) for p in urlpatterns if 'api' in str(p.pattern)]
    print(f"   API routes found: {len(api_routes)}")
    for route in api_routes:
        print(f"     - {route}")
        
except Exception as e:
    print(f"   ERROR: {e}")

# Check ViewSet
print("\n5. ViewSet Check")
try:
    from core.views import MeetingViewSet
    print(f"   MeetingViewSet: ✓")
    print(f"   Serializer: {MeetingViewSet.serializer_class}")
    print(f"   Permission: {MeetingViewSet.permission_classes}")
except Exception as e:
    print(f"   ERROR: {e}")

# Check Serializer
print("\n6. Serializer Check")
try:
    from core.serializers import MeetingSerializer
    print(f"   MeetingSerializer: ✓")
    print(f"   Fields: {MeetingSerializer.Meta.fields}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test API endpoint
print("\n7. API Endpoint Test")
try:
    client = APIClient()
    
    # Try to access meetings endpoint without auth
    response = client.get('/api/meetings/')
    print(f"   GET /api/meetings/ (no auth): {response.status_code}")
    
    # Create a test user and try with auth
    if user_count > 0:
        user = User.objects.first()
        client.force_authenticate(user=user)
        response = client.get('/api/meetings/')
        print(f"   GET /api/meetings/ (with auth): {response.status_code}")
        if response.status_code == 200:
            print(f"   Response data: {response.data}")
    
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check template
print("\n8. Template Check")
import os
template_path = os.path.join(os.path.dirname(__file__), 'templates', 'meetings.html')
template_improved = os.path.join(os.path.dirname(__file__), 'templates', 'meetings_improved.html')

if os.path.exists(template_path):
    print(f"   meetings.html: ✓ (exists)")
else:
    print(f"   meetings.html: ✗ (NOT FOUND)")
    
if os.path.exists(template_improved):
    print(f"   meetings_improved.html: ✓ (exists)")
else:
    print(f"   meetings_improved.html: ✗ (NOT FOUND)")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)

# Recommendations
print("\n📋 RECOMMENDATIONS:")

if count == 0:
    print("   ⚠️  No meetings in database - create some test meetings")

if user_count == 0:
    print("   ⚠️  No users in database - run: python manage.py createsuperuser")

print("\n✅ Next steps:")
print("   1. Run: python manage.py migrate")
print("   2. Run: python manage.py createsuperuser (if needed)")
print("   3. Start server: python manage.py runserver")
print("   4. Visit: http://127.0.0.1:8000/meetings/")
print()
