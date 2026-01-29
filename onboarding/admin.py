from django.contrib import admin
from .models import OnboardingStep

@admin.register(OnboardingStep)
class OnboardingStepAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_completed', 'interests_completed', 'goals_completed', 'community_completed', 'is_completed']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['user__username']
