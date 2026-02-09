#!/usr/bin/env python3
"""
Verification script for Unity Circles fixes
Checks that all required files exist and are properly configured
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ MISSING {description}: {filepath}")
        return False

def check_file_contains(filepath, search_string, description):
    """Check if a file contains a specific string"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ MISSING {description}")
                return False
    except Exception as e:
        print(f"❌ ERROR checking {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("Unity Circles - Fix Verification")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check 1: Post detail template
    print("1. Checking Post Detail Template Fix...")
    all_checks_passed &= check_file_exists(
        "templates/post_detail.html",
        "Post detail template"
    )
    print()
    
    # Check 2: Messages privacy fix
    print("2. Checking Messages Privacy Fix...")
    all_checks_passed &= check_file_contains(
        "chat/views.py",
        "users_with_conversations",
        "Privacy filter in messages_page()"
    )
    all_checks_passed &= check_file_contains(
        "chat/views.py",
        "get_all_users_for_new_chat",
        "New chat endpoint in chat/views.py"
    )
    all_checks_passed &= check_file_contains(
        "chat/urls.py",
        "get_all_users_for_new_chat",
        "New chat URL in chat/urls.py"
    )
    all_checks_passed &= check_file_contains(
        "templates/messages.html",
        "showNewChatModal",
        "New chat button in messages.html"
    )
    print()
    
    # Check 3: Meeting API fix
    print("3. Checking Meeting API Fix...")
    all_checks_passed &= check_file_contains(
        "core/views.py",
        "class MeetingViewSet",
        "MeetingViewSet in core/views.py"
    )
    all_checks_passed &= check_file_contains(
        "core/views.py",
        "get_users_for_meeting",
        "get_users_for_meeting() in core/views.py"
    )
    all_checks_passed &= check_file_contains(
        "core/urls.py",
        "DefaultRouter",
        "API router in core/urls.py"
    )
    all_checks_passed &= check_file_contains(
        "core/urls.py",
        "router.register(r'meetings'",
        "Meeting routes registered"
    )
    print()
    
    # Check 4: Models exist
    print("4. Checking Required Models...")
    all_checks_passed &= check_file_contains(
        "core/models.py",
        "class Meeting",
        "Meeting model"
    )
    all_checks_passed &= check_file_contains(
        "core/models.py",
        "class Post",
        "Post model"
    )
    all_checks_passed &= check_file_contains(
        "core/models.py",
        "class PostComment",
        "PostComment model"
    )
    all_checks_passed &= check_file_contains(
        "chat/models.py",
        "class DirectMessage",
        "DirectMessage model"
    )
    print()
    
    # Check 5: Serializers exist
    print("5. Checking Serializers...")
    all_checks_passed &= check_file_contains(
        "core/serializers.py",
        "class MeetingSerializer",
        "MeetingSerializer"
    )
    print()
    
    # Summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED! All fixes are in place.")
        print()
        print("You can now run:")
        print("  python manage.py runserver")
        print()
        print("And test:")
        print("  1. Post detail pages and voting")
        print("  2. Messages privacy (only shows conversations)")
        print("  3. New chat button (to start new conversations)")
        print("  4. Meeting scheduling")
    else:
        print("❌ SOME CHECKS FAILED! Please review the errors above.")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
