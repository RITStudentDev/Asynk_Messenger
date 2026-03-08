from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MessageSerializer
from django_q.tasks import async_task
import uuid

from .models import Message
from .tasks import process_pending_messages 

class MessageViewSet(viewsets.ViewSet):
        
    def create(self, request):
        serializer = MessageSerializer
        if serializer.is_valid():
            message = serializer.save(messageId=uuid.uuid4())
            task_id = async_task(process_pending_messages, message.messageId)
            return Response(
                {'success': True, 'messageId': message.messageId, 'taskId': task_id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    @action(detail=False, methods=['get'], url_path='convo/(?P<user_id>[^/.]+)')
    def get_messages(self, request, user_id=None, other_user_id=None):
        from django.db.models import Q

        messages = Message.objects.filter(
            Q(senderId=user_id, receiverId=other_user_id) |
            Q(senderId=other_user_id, receiverId=user_id)
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response({'message': list(messages)})
    
    class RoomViewSet(viewsets.ViewSet):

        def create():
            pass