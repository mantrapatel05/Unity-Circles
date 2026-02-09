from rest_framework import serializers
from .models import DirectMessage
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class DirectMessageSerializer(serializers.ModelSerializer):
    sender = UserMinimalSerializer(read_only=True)
    receiver = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'content', 'created_at']
        read_only_fields = ['created_at']
