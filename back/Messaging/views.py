from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_q.tasks import async_task
from django.db.models import Q
import uuid

from .models import Message
from .tasks import process_pending_messages 

class MessageViewSet(viewsets.ViewSet):
        
    def create(self, request):
        required_fields = ['receiverId', 'senderId', 'content']

        if not all(field in request.data for field in required_fields):
            return Response(
                {'error': 'Missing required fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        message = Message.objects.create(
            messageId=uuid.uuid4(),
            senderId=request.data['senderId'],
            receiverId=request.data['receiverId'],
            content=request.data['content']
        )
        task_id = async_task(process_pending_messages, message.messageId)

        return Response(
            {
                'success': True,
                'messageId': message.messageId,
                'taskId': task_id
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_messages(self, request, user_id=None, other_user_id=None):

        messages = Message.objects.filter(
            Q(senderId=user_id, receiverId=other_user_id) |
            Q(senderId=other_user_id, receiverId=user_id)
        ).values(
            'messageId',
            'senderId',
            'content',
            'timestamp',
            'status'
        ).order_by('timestamp')

        return Response({'message': list(messages)})