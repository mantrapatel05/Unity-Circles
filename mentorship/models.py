from django.db import models
from django.contrib.auth.models import User

class MentorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="mentor_profile"
    )
    field = models.CharField(max_length=100)
    expertise = models.TextField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
