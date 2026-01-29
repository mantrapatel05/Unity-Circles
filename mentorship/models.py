from django.db import models
from django.contrib.auth.models import User

class MentorshipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_requests_sent')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_requests_received')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} -> {self.mentor.username}: {self.subject}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('student', 'mentor')


class Mentorship(models.Model):
    request = models.OneToOneField(MentorshipRequest, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    goals = models.TextField(blank=True)
    progress = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.request.student.username} - {self.request.mentor.username}"
    
    class Meta:
        ordering = ['-start_date']
