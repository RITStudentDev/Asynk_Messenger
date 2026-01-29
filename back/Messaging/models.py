from django.db import models

# Create your models here.
class Message(models.Model):

    MESSAGE_STATUS = [
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    messageId = models.CharField(max_length=255, unique=True, primary_key=True)
    receiverId = models.CharField(max_length=255)
    senderId = models.CharField(max_length=255)
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