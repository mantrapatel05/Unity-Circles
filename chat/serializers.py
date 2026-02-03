from rest_framework import serializers
from .models import ChatRoom, Message
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'created_at']
        read_only_fields = ['created_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    members = UserMinimalSerializer(many=True, read_only=True)
    messages_count = serializers.SerializerMethodField()
    
    def get_messages_count(self, obj):
        return obj.messages.count()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'description', 'members', 'messages', 'messages_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
