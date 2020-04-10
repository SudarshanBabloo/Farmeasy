from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from user_auth.models import Message,consumer

class ChatConsumer(WebsocketConsumer):
    def message_to_json(self, message):
        return {
            'author': message.author.email,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
    

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def fetch_messages(self,data):
        messages = Message.last_10_messages(self)
        t=self.messages_to_json(messages)
        content = {
            'command': 'messages',
            'messages': t
        }
        self.send_message(content)

    
    

    def new_message(self, data):
        author = data['from']
        author_user = consumer.objects.filter(email=author)[0]
        message = Message.objects.create(
            author=author_user, 
            content=data['message'])
        print(author)
        print(data['message'])    
        
        t=[]
        t=self.message_to_json(message)
        content = {
            'command': 'new_message',
            'message': t
        }
        return self.send_chat_message(content)

    
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        print('hii klm')
        print('hii klm')
        print('hii klm')
        print('hii klm')
        data = json.loads(text_data)
        self.commands[data['command']](self,data)
        

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        print(message)
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))