import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Recieve message from socket
    async def receive(self, text_data=None, bytes_data=None):
        message_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                'type': 'chat_message',
                'content': message_data_json['message'],
                'sender_username': message_data_json['sender_username'],
                'timestamp' : message_data_json['timestamp'],
             }
        )

    # Recieve message from group room
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
                'content': event['content'],
                'sender_username': event['sender_username'],
                'timestamp': event['timestamp']
            }))
        