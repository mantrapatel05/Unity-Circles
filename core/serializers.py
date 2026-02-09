from rest_framework import serializers
from .models import Community, Post, PostComment, Meeting
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class PostCommentSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = PostComment
        fields = ['id', 'author', 'content', 'upvotes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    class Meta:
        model = Post
        fields = ['id', 'community', 'author', 'title', 'content', 'upvotes', 'downvotes', 'comments_count', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CommunitySerializer(serializers.ModelSerializer):
    members = UserMinimalSerializer(many=True, read_only=True)
    creator = UserMinimalSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    
    def get_members_count(self, obj):
        return obj.members.count()
    
    def get_posts_count(self, obj):
        return obj.posts.count()
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'category', 'members', 'members_count', 'creator', 'image', 'posts_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MeetingSerializer(serializers.ModelSerializer):
    mentor = UserMinimalSerializer(read_only=True)
    attendees = UserMinimalSerializer(many=True, read_only=True)
    attendees_count = serializers.SerializerMethodField()
    community_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    def get_attendees_count(self, obj):
        return obj.attendees.count()
    
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description', 'mentor', 'community', 'attendees', 'attendees_count', 'scheduled_time', 'duration_minutes', 'status', 'zoom_link', 'community_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'community']
