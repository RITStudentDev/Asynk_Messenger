from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=9, blank=True, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username