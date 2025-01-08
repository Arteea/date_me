from channels.generic.websocket import AsyncWebsocketConsumer
import json
import pika
from .models import Dialog


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.dialog_id = self.scope['url_route']['kwargs']['dialog_id']
        self.room_group_name = f"chat_{self.dialog_id}"

        # Добавляем WebSocket в группу
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        # Удаляем WebSocket из группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    

    async def send_message_to_queue(self,message,user_id,dialog_id):
        credentials = pika.PlainCredentials(username='rmuser',password='rmpassword')
        params=pika.ConnectionParameters(host='127.0.0.1',port='5672',credentials=credentials)
        connection = pika.BlockingConnection(params)
        channel=connection.channel()

        channel.exchange_declare(exchange="dialog_exchange",exchange_type="direct",durable=True)

        routing_key=f"dialog_{dialog_id}"

        message_data = {
            "message" :message,
            'user_id': user_id,
            "dialog_id": dialog_id,
        }
        
        channel.basic_publish(exchange='dialog_exchange', routing_key=routing_key, body=json.dumps(message_data))

        connection.close()





    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']
        dialog_id=self.dialog_id
        print(message)

        await self.send_message_to_queue(message=message,user_id=user_id,dialog_id=dialog_id)

        # Отправляем сообщение группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    

    async def chat_message(self, event):
        message = event['message']

        # Отправляем сообщение обратно WebSocket-клиенту
        await self.send(text_data=json.dumps({
            'message': message
        }))