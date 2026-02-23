import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
    async def receive(self, message_data):
        message_data_json = json.loads(message_data)
        message = message_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                'type': 'chat_message',
                'message': message
             }
        )

    # Recieve message from group room
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message':message}))
        