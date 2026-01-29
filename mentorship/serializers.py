from rest_framework import serializers
from .models import MentorshipRequest, Mentorship
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class MentorshipRequestSerializer(serializers.ModelSerializer):
    student = UserMinimalSerializer(read_only=True)
    mentor = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = MentorshipRequest
        fields = ['id', 'student', 'mentor', 'subject', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MentorshipSerializer(serializers.ModelSerializer):
    request = MentorshipRequestSerializer(read_only=True)
    
    class Meta:
        model = Mentorship
        fields = ['id', 'request', 'start_date', 'end_date', 'goals', 'progress']
