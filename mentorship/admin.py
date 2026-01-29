from django.contrib import admin
from .models import MentorshipRequest, Mentorship

@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'mentor', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__username', 'mentor__username', 'subject']

@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    list_display = ['request', 'start_date', 'end_date']
    list_filter = ['start_date']
    search_fields = ['request__student__username', 'request__mentor__username']
