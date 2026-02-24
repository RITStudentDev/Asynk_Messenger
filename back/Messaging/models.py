from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):

    MESSAGE_STATUS = [
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    messageId = models.CharField(max_length=255, unique=True, primary_key=True)
    receiverId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    mediaUrl = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=MESSAGE_STATUS, default='pending')
    retryCount = models.IntegerField(default=0)
    lastTriedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Message {self.messageId} from {self.sender} to {self.receiver}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['status', 'timestamp']),
            models.Index(fields=['receiverId', 'status']),
        ]