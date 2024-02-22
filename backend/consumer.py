from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

import json

class CountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "count_room"
        self.room_group_name = f"count_group_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected to WebSocket.'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        print('message', message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_to_frontend',
                'message': f'Received: {message}'
            }
        )

    async def send_to_frontend(self, event):
        await self.send(text_data=json.dumps(event))


class POSextended(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = "extended_group"
        self.room_group_name ="extended_group"
        # self.room_group_name = f"extended_group%_"  % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected to WebSocket.'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        print('message', message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_to_frontend',
                'message': f'Received: {message}'
            }
        )

    async def send_to_frontend(self, event):
        await self.send(text_data=json.dumps(event))

    async def Send_to_front_end_extended(self, event):
        print('dataetasdad', event['data'])
        data = event['data']
        await self.send(text_data=json.dumps(data))
