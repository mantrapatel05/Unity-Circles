from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MentorshipRequest, Mentorship, MentorProfile

class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = MentorProfile
        fields = ['id', 'user', 'field', 'expertise', 'bio', 'is_active']


class MentorshipRequestSerializer(serializers.ModelSerializer):
    student = UserMinimalSerializer(read_only=True)
    mentor = UserMinimalSerializer(read_only=True)

    class Meta:
        model = MentorshipRequest
        fields = ['id', 'student', 'mentor', 'subject', 'description', 'status', 'created_at', 'updated_at']


class MentorshipSerializer(serializers.ModelSerializer):
    request = MentorshipRequestSerializer(read_only=True)

    class Meta:
        model = Mentorship
        fields = ['id', 'request', 'start_date', 'end_date', 'goals', 'progress']
