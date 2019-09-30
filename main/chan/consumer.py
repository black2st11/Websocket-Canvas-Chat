from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class DrawConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chan_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async  def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        if 'message' in text_data:
            message = text_data_json['message']
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'message': message,
                    'type': 'chat_message'
                }
            )
        if 'x' in text_data:
            pointX = text_data_json['x']
            pointY = text_data_json['y']
            actType = text_data_json['type']
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'x': pointX,
                    'y': pointY,
                    'actType': actType,
                    'type': 'draw_message',
                })


    async def draw_message(self,event):
        pointX = event['x']
        pointY = event['y']
        actType = event['actType']

        await self.send(text_data=json.dumps({
            'x':pointX,
            'y':pointY,
            'actType' : actType
        }))

    async def chat_message(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message' : message
        }))





