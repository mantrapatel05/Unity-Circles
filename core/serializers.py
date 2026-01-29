from rest_framework import serializers
from .models import Community
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class CommunitySerializer(serializers.ModelSerializer):
    members = UserMinimalSerializer(many=True, read_only=True)
    creator = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'category', 'members', 'creator', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
