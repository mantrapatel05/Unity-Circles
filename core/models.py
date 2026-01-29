from django.db import models
from django.contrib.auth.models import User

class Community(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('business', 'Business'),
        ('arts', 'Arts'),
        ('science', 'Science'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    members = models.ManyToManyField(User, related_name='communities')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    image = models.ImageField(upload_to='community_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Communities'
