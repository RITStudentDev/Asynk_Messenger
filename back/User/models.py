from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=255, unique=True, primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username