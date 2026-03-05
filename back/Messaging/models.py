from django.db import models
from django.conf import settings
class Message(models.Model):

    MESSAGE_STATUS = [
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    messageId = models.UUIDField(max_length=255, unique=True, primary_key=True)
    receiverId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    senderId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
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

    
class Room(models.Model):
    roomId = models.CharField(primary_key=True, unique=True, max_length=16)
    roomName = models.CharField(max_length=50)
    icon = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_rooms')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='RoomMembership', related_name='rooms')
    timeCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timeCreated']      

    def __str__(self):
        return f'{self.name} ({self.roomId})' 
    
class RoomMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')

    def __str__(self):
        return f'{self.user} in {self.room}'