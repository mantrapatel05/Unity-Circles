#!/usr/bin/env python
"""
Quick fix for Django 5.1 + Python 3.14 AttributeError
Run this script to patch all admin files
"""

import os
import sys

ADMIN_FILES = {
    'accounts/admin.py': '''from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import StudentProfile

class StudentProfileChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone_number', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_changelist(self, request, **kwargs):
        return StudentProfileChangeList
''',
    
    'chat/admin.py': '''from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import DirectMessage

class DirectMessageChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'created_at']
    list_filter = ['created_at', 'sender', 'receiver']
    search_fields = ['content', 'sender__username', 'receiver__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_changelist(self, request, **kwargs):
        return DirectMessageChangeList
''',
    
    'core/admin.py': '''from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Community

class CommunityChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at', 'members_count']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['members']
    
    def get_changelist(self, request, **kwargs):
        return CommunityChangeList
    
    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = 'Members'
''',
    
    'onboarding/admin.py': '''from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import OnboardingStep

class OnboardingStepChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(OnboardingStep)
class OnboardingStepAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_completed', 'interests_completed', 'goals_completed', 'community_completed', 'is_completed']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['user__username']
    
    def get_changelist(self, request, **kwargs):
        return OnboardingStepChangeList
''',
    
    'mentorship/admin.py': '''from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import MentorProfile

class MentorProfileChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return MentorProfileChangeList
'''
}

def main():
    print("=" * 50)
    print("Django Admin Python 3.14 Compatibility Patch")
    print("=" * 50)
    print()
    
    for filepath, content in ADMIN_FILES.items():
        if os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
        else:
            print(f"✗ Not found: {filepath}")
    
    print()
    print("=" * 50)
    print("All admin files patched!")
    print("=" * 50)
    print()
    print("Now run:")
    print("  python manage.py runserver")
    print()

if __name__ == '__main__':
    main()
