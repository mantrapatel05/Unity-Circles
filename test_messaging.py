#!/usr/bin/env python
"""
Test script for Unity Circles messaging system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unity_circles.settings')
django.setup()

from django.contrib.auth.models import User
from chat.models import DirectMessage

def test_messaging_system():
    print("=" * 60)
    print("Unity Circles - Messaging System Test")
    print("=" * 60)
    
    # Test 1: Check if models are working
    print("\n1. Testing DirectMessage model...")
    try:
        count = DirectMessage.objects.count()
        print(f"   ✓ DirectMessage model working - {count} messages in database")
    except Exception as e:
        print(f"   ✗ Error with DirectMessage model: {e}")
        return False
    
    # Test 2: Check if users exist
    print("\n2. Checking users...")
    try:
        user_count = User.objects.count()
        print(f"   ✓ Found {user_count} users in database")
        
        if user_count == 0:
            print("   ! Creating test users...")
            user1 = User.objects.create_user(
                username='testuser1', 
                password='testpass123',
                email='test1@example.com'
            )
            user2 = User.objects.create_user(
                username='testuser2', 
                password='testpass123',
                email='test2@example.com'
            )
            print(f"   ✓ Created test users: {user1.username} and {user2.username}")
        else:
            users = User.objects.all()[:5]
            print("   Users:")
            for user in users:
                print(f"      - {user.username} (ID: {user.id})")
    except Exception as e:
        print(f"   ✗ Error checking users: {e}")
        return False
    
    # Test 3: Try creating a test message
    print("\n3. Testing message creation...")
    try:
        users = User.objects.all()[:2]
        if len(users) >= 2:
            message = DirectMessage.objects.create(
                sender=users[0],
                receiver=users[1],
                content="This is a test message!"
            )
            print(f"   ✓ Created test message from {users[0].username} to {users[1].username}")
            print(f"   Message ID: {message.id}, Created at: {message.created_at}")
            
            # Delete the test message
            message.delete()
            print("   ✓ Test message deleted")
        else:
            print("   ! Not enough users to test message creation")
    except Exception as e:
        print(f"   ✗ Error creating message: {e}")
        return False
    
    # Test 4: Check message queries
    print("\n4. Testing message queries...")
    try:
        if user_count > 0:
            user = User.objects.first()
            sent = DirectMessage.objects.filter(sender=user).count()
            received = DirectMessage.objects.filter(receiver=user).count()
            print(f"   ✓ User '{user.username}' has sent {sent} and received {received} messages")
    except Exception as e:
        print(f"   ✗ Error with message queries: {e}")
        return False
    
    # Test 5: Check database structure
    print("\n5. Checking database structure...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(chat_directmessage);")
            columns = cursor.fetchall()
            print("   ✓ chat_directmessage table columns:")
            for col in columns:
                print(f"      - {col[1]} ({col[2]})")
    except Exception as e:
        print(f"   ✗ Error checking database: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nThe messaging system is working correctly!")
    print("\nTo use the system:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/chat/")
    print("3. Login and start messaging!")
    print("\nAPI Endpoints available at:")
    print("- GET  /chat/api/messages/           - List all messages")
    print("- POST /chat/api/messages/           - Create a message")
    print("- GET  /chat/api/messages/conversations/ - List conversations")
    print("- GET  /chat/api/messages/with_user/?user_id=X - Get conversation")
    print("- POST /chat/api/send/               - Send a message")
    print("- GET  /chat/api/users/              - List all users")
    
    return True

if __name__ == '__main__':
    success = test_messaging_system()
    sys.exit(0 if success else 1)
