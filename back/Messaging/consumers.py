import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    # Recieve message from socket
    def receive(self, text_data=None, bytes_data=None):
        message_data_json = json.loads(text_data)
        message = message_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                'type': 'chat_message',
                'message': message
             }
        )

    # Recieve message from group room
    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({'message':message}))
        