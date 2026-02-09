from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import OnboardingStep

class OnboardingStepChangeList(ChangeList):
    """Fix Python 3.14 compatibility"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(OnboardingStep)
class OnboardingStepAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_completed', 'interests_completed', 'goals_completed', 'community_completed', 'is_completed']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['user__username']
    
    def get_changelist(self, request, **kwargs):
        return OnboardingStepChangeList
