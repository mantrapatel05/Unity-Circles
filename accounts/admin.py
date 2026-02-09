from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import StudentProfile

class StudentProfileChangeList(ChangeList):
    """Fix Python 3.14 compatibility"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone_number', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_changelist(self, request, **kwargs):
        return StudentProfileChangeList
