from django.db import models
from django.contrib.auth.models import User

class DirectMessage(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dm_sent"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dm_received"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_directmessage'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
