import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, Course, User
from asgiref.sync import sync_to_async
from .utils import describtion_to_html

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope["url_route"]["kwargs"]["course_id"]
        self.room_group_name = f"chat_{self.course_id}"

        # Guruhga qo‘shish
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
    
    # Xabarni frontga yuborish
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @sync_to_async
    def save_message(self, course_id, auth_token, content):
        course = Course.objects.get(id=course_id)
        user = User.objects.get(auth_token=auth_token)
        return ChatMessage.objects.create(course=course, user=user, content=content)
