from channels.generic.websocket import AsyncWebsocketConsumer
import json
import aio_pika
from .models import Dialog,Message
from users.models import User

from asgiref.sync import sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        ###Определяем dialog_id через url
        self.dialog_id = self.scope['url_route']['kwargs']['dialog_id']
        
        self.room_group_name = f"chat_{self.dialog_id}"

        ###Добавляем соединение(room_group_name и channel_name) в группу
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        ###Подтверждаем соединение
        await self.accept()


    
    async def disconnect(self,*args):
        ###Удаляем соединение из группы
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        print(*args)
        print(f"Disconnected with code: {args}")
        



    async def receive(self,text_data):

        data=json.loads(text_data)
        message=data['message']
        user_id=data['user_id']
        dialog_id=self.dialog_id

        ###Отправка сообщения в обменник RMQ для добавления в PostgreSQl
        # await self.send_message_to_queue(message,user_id,dialog_id)

        await self.save_to_database(message,user_id,dialog_id)

        await self.channel_layer.group_send(self.room_group_name,{'type':'chat_message','message':message})


    async def chat_message(self,event):
        print(event)
        message = event['message']
        await self.send(text_data=json.dumps({'message':message}))




    async def send_message_to_queue(self,message,user_id,dialog_id):
        # credentials = aio_pika.PlainCredentials(username='rmuser',password='rmpassword')
        connection = await aio_pika.connect_robust(host='127.0.0.1',port=5672,login='rmuser',password='rmpassword')
        async with connection:
            channel=await connection.channel()

            exchange = await channel.declare_exchange("dialog_exchange",aio_pika.ExchangeType.DIRECT ,durable=True)

            queue_name = "general_dialog_queue"
            queue = await channel.declare_queue(queue_name, durable=True)

            routing_key=f"dialog_{dialog_id}"
            print(routing_key)
            message_data = {
                "message" :message,
                'user_id': user_id,
                "dialog_id": dialog_id,
            }
            print(message_data)
            await exchange.publish(aio_pika.Message(body=json.dumps(message_data).encode()), routing_key=routing_key)

        
    async def save_to_database(self,message,user_id,dialog_id):
        dialog = await sync_to_async(Dialog.objects.get,thread_sensitive=False)(id=dialog_id)
        user = await sync_to_async(User.objects.get,thread_sensitive=False)(id=user_id)
        await sync_to_async(Message.objects.create,thread_sensitive=False)(dialog_id=dialog,author_id=user,body=message)
        print(f"Message_saved: {message}")























    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     message = data['message']
    #     user_id = data['user_id']
    #     dialog_id=self.dialog_id
    #     print(message)

    #     await self.send_message_to_queue(message=message,user_id=user_id,dialog_id=dialog_id)

    #     # Отправляем сообщение группе
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )
    

    # async def chat_message(self, event):
    #     message = event['message']

    #     # Отправляем сообщение обратно WebSocket-клиенту
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))