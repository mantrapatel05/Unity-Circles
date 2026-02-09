from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import DirectMessage

class DirectMessageChangeList(ChangeList):
    """Custom ChangeList to fix Python 3.14 compatibility issue"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'created_at']
    list_filter = ['created_at', 'sender', 'receiver']
    search_fields = ['content', 'sender__username', 'receiver__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_changelist(self, request, **kwargs):
        """Override to use custom ChangeList"""
        return DirectMessageChangeList
