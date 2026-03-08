from rest_framework import serializers
from .models import Message, Room

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['messageId', 'senderId', 'recieverId', 'content', 'timestamp', 'status']
        read_only_fields = ['messageId', 'timestamp', 'status']