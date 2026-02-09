from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Community

class CommunityChangeList(ChangeList):
    """Fix Python 3.14 compatibility"""
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
