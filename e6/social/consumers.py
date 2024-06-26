import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from .models import *

@sync_to_async
def getroom(chat_id, user_id):
    return Room.objects.filter(id=chat_id, members__in=[user_id,])

@sync_to_async
def createmsg(sender, text, room_id):
    return Message.objects.create(sender=sender, text=text, room_id=room_id)

@sync_to_async
def getuser(username):
    user = User.objects.get(username=username)
    return user

class MessageConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        chat_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = chat_id
        room = getroom(chat_id, self.scope['user'].id)
        if room:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.dispatch()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'deluser' in text_data_json:
            await self.channel_layer.group_send(self.group_name, {'type':'send_message', 'message':{'kickuser':text_data_json['deluser']}})
            return
        text = text_data_json['message']
        sender = self.scope['user']
        message = await createmsg(sender=sender, text=text, room_id=int(self.scope['url_route']['kwargs']['room_id']))
        event = {
            'type': 'send_message',
            'message': {
                'text': text,
                'sender': sender.username,
                'time': message.time.isoformat(),
                'sendername':sender.first_name,
            }
        }
        await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):
        message = event['message']
        if 'kickuser' in message:
            if self.scope['user'].username == message['kickuser']:
                await self.close()
            return
        await self.send(text_data=json.dumps({'message':message}))
