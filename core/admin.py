from django.contrib import admin
from .models import Community

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at', 'members_count']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['members']
    
    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = 'Members'
