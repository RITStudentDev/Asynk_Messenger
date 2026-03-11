from rest_framework import serializers
from .models import Message, Room, RoomMembership

class MessageSerializer(serializers.ModelSerializer):

    sender_username = serializers.CharField(source='senderId.username', read_only=True)

    class Meta:
        model = Message
        fields = ['messageId', 'senderId', 'sender_username', 'receiverId', 'room', 'content', 'timestamp', 'status']
        read_only_fields = ['messageId', 'timestamp', 'status', 'senderId']

class RoomMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = RoomMembership
        fields = ['user', 'username', 'role']
        read_only_fields = ['joined_at']

class RoomSerializer(serializers.ModelSerializer):
    members = RoomMembershipSerializer(source='memberships', many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    member_count = serializers.SerializerMethodField()

    def get_member_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        request = self.context.get('request')
        room = Room.objects.create(owner=request.user, **validated_data)
        RoomMembership.objects.create(user=request.user, room=room)
        return room

    class Meta:
        model = Room
        fields = ['roomId', 'roomName', 'icon', 'bio', 'owner', 'members', 'member_count', 'timeCreated']
        read_only_fields = ['roomId', 'timeCreated', 'owner']