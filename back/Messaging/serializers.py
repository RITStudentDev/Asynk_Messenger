from rest_framework import serializers
from .models import Message, Room, RoomMembership

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['messageId', 'senderId', 'recieverId', 'content', 'timestamp', 'status']
        read_only_fields = ['messageId', 'timestamp', 'status']

class RoomMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = RoomMembership
        fields = ['user', 'username', 'joined_at', 'role']
        read_only_fields = ['joined_at']

class RoomSerializer(serializers.ModelSerializer):

    members = RoomMembershipSerializer(source='memberships', many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['roomId', 'roomId', 'icon', 'bio', 'owner', 'members', 'member_count', 'timeCreated']
        read_only_fields = ['timeCreated', 'owner']
        