from django.db import models

# Create your models here.
class UnsentMessage(models.Model):
    messageId = models.CharField(max_length=255, unique=True, primary_key=True)
    recieverId = models.CharField(max_length=255)
    senderId = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.messageId} from {self.senderId} to {self.recieverId}"