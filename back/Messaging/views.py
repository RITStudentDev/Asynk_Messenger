from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MessageSerializer, RoomSerializer, RoomMembershipSerializer
from .models import Room, Message
from rest_framework.permissions import IsAuthenticated
from User.views import CookieJWTAuthentication
from django_q.tasks import async_task
import uuid

from .models import Message
from .tasks import process_pending_messages 

class MessageViewSet(viewsets.ViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
        
    def create(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            message = serializer.save(senderId=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    
    # POST /rooms/
    def create(self, request):
        serializer = RoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            room = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # GET /rooms/
    def list(self, request):
        rooms = Room.objects.filter(members=request.user)
        serializer = RoomSerializer(rooms, many=True)
        return Response({'rooms': serializer.data})

    # GET /rooms/{roomId}
    def retrieve(self, request, pk=None):
        try:
            room=Room.objects.get(roomId=pk)
        except Room.DoesNotExist:
            return Response({'error': 'Room not does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if not room.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a memeber of this room'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    
    # GET /rooms/{roomId}/messages/
    @action(detail=True, methods=['get'], url_path='messages')
    def get_room_messages(self, request, pk=None):
        try:
            room=Room.objects.get(roomId=pk)
        except Room.DoesNotExist:
            return Response({'error': 'Room not does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if not room.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a memeber of this room'}, status=status.HTTP_403_FORBIDDEN)
        
        messages = Message.objects.filter(roomId=pk).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response({'messages': serializer.data})
        

