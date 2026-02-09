from django.db import models
from django.contrib.auth.models import User

class OnboardingStep(models.Model):
    STEP_CHOICES = [
        ('profile', 'Profile Setup'),
        ('interests', 'Interests'),
        ('goals', 'Goals'),
        ('community', 'Community'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_completed = models.BooleanField(default=False)
    interests_completed = models.BooleanField(default=False)
    goals_completed = models.BooleanField(default=False)
    community_completed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Onboarding"
    
    def check_completion(self):
        if all([self.profile_completed, self.interests_completed, self.goals_completed, self.community_completed]):
            self.is_completed = True
        else:
            self.is_completed = False
        self.save()
    
    class Meta:
        ordering = ['-created_at']
