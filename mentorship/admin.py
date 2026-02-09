from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import MentorProfile

class MentorProfileChangeList(ChangeList):
    """Fix Python 3.14 compatibility"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return MentorProfileChangeList
