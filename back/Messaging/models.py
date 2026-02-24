from django.db import models
from django.contrib.auth.models import User

class room(models.Model):
    roomId = models.CharField(max_length=16, unique=True, primary_key=True)
    roomName = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='rooms')


class Message(models.Model):

    MESSAGE_STATUS = [
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    messageId = models.CharField(max_length=255, unique=True, primary_key=True)
    receiverId = models.ForeignKey(max_length=255, to=User, on_delete=models.CASCADE)
    senderId = models.ForeignKey(max_length=255, to=User, on_delete=models.CASCADE)
    content = models.TextField()
    mediaUrl = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=MESSAGE_STATUS, default='pending')
    retryCount = models.IntegerField(default=0)
    lastTriedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Message {self.messageId} from {self.senderId} to {self.receiverId}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['status', 'timestamp']),
            models.Index(fields=['receiverId', 'status']),
        ]