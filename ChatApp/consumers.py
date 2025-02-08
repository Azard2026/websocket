import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ChatApp.models import *
import datetime
from django.utils.timezone import localtime






class OneToOneChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['user1']
        self.user2 = self.scope['url_route']['kwargs']['user2']

        # Sort user names to ensure consistent room name
        sorted_users = sorted([self.user1, self.user2])
        self.room_name = f"room_{sorted_users[0]}_{sorted_users[1]}"

        # Get or create the room
        self.room = await self.get_or_create_room(sorted_users[0], sorted_users[1])

        # Add this connection to the room's group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']

        # Save the message in the database
        await self.save_message(self.room, sender, message)

        # Broadcast the message to the room
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': {
                    'sender': sender,
                    'message': message,
                    'timestamp': self.get_timestamp(),
                },
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))

    @database_sync_to_async
    def get_or_create_room(self, user1, user2):
        return ChatRoom.objects.get_or_create(user1=user1, user2=user2)[0]

    @database_sync_to_async
    def save_message(self, room, sender, message):
        singleMessage.objects.create(room=room, sender=sender, message=message)

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CallConsumergroup(AsyncWebsocketConsumer): 
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        # Join the call group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the call group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Handle incoming call notification
        if data.get('type') == 'call_initiated':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'incoming_call',
                    'caller': data['caller'],
                }
            )
        else:
            # Broadcast signaling data (offer, answer, ICE candidates)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_message',
                    'message': data,
                }
            )

    async def call_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def incoming_call(self, event):
        await self.send(text_data=json.dumps({
            'type': 'incoming_call',
            'caller': event['caller'],
        })) 

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Notify the receiver about the incoming call
        if data.get('type') == 'call_initiated':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'incoming_call',
                    'caller': data['caller'],  # Notify the receiver
                }
            )
        else:
            # Broadcast signaling data (offer, answer, ICE candidates)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_message',
                    'message': data,
                }
            )

    async def call_message(self, event):
        # Send signaling data to WebSocket
        await self.send(text_data=json.dumps(event['message']))

    async def incoming_call(self, event):
        # Notify the client about the incoming call
        await self.send(text_data=json.dumps({
            'type': 'incoming_call',
            'caller': event['caller'],
        }))

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        # Join the call group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the call group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Broadcast signaling data to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data,
            }
        )

    async def call_message(self, event):
        # Send signaling data to WebSocket
        await self.send(text_data=json.dumps(event['message']))


class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'data': data,
                'sender_channel_name': self.channel_name
            }
        )

    async def call_message(self, event):
        if event['sender_channel_name'] != self.channel_name:
            await self.send(text_data=json.dumps(event['data']))