from rest_framework import serializers
from .models import OnboardingStep
from django.contrib.auth.models import User


class OnboardingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingStep
        fields = ['id', 'user', 'profile_completed', 'interests_completed', 'goals_completed', 'community_completed', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
