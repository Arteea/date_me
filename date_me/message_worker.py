import aio_pika
import json
import asyncio

from asgiref.sync import sync_to_async


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'date_me.settings')
django.setup()


from dialogs.models import Message, Dialog
from users.models import User
from django.core.exceptions import ObjectDoesNotExist




async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        print(f"Обработано сообщение {data}")
        dialog_id=data['dialog_id']
        user_id = data['user_id']
        message_body = data['message']
        print(f"Received message from {user_id} for dialog {dialog_id}: {message_body}")
        
        try:
            routing_key = f"dialog_{dialog_id}"
            queue_name = "general_dialog_queue"
            
            dialog = await sync_to_async(Dialog.objects.get,thread_sensitive=False)(id=dialog_id)
            user = await sync_to_async(User.objects.get,thread_sensitive=False)(id=user_id)

            await sync_to_async(Message.objects.create,thread_sensitive=False)(dialog_id=dialog,author_id=user,body=message_body)
            print(f"Message_saved: {message_body}")
        except ObjectDoesNotExist as e:
            print(f"Error - {e}")




async def main():
    # credentials = aio_pika.PlainCredentials(username='rmuser',password='rmpassword')
    connection = await aio_pika.connect_robust(host='127.0.0.1',port=5672,login='rmuser',password='rmpassword')
    
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange("dialog_exchange",aio_pika.ExchangeType.DIRECT,durable=True)

        queue_name = "general_dialog_queue"

        queue = await channel.declare_queue(queue_name, durable=True)

        await queue.bind(exchange)
        print("Waiting for messages ...")


        await queue.consume(callback)

        await asyncio.Future()


if __name__=="__main__":
    # import os
    # import django

    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'date_me.settings')
    # django.setup()

    asyncio.run(main())
             
        












# def callback(ch, method, properties, body):
#         message_data = json.loads(body)
#         dialog_id = message_data['dialog_id']
#         user_id = message_data['user_id']
#         message_body = message_data['message']
#         print(f"Received message from {user_id} for dialog {dialog_id}: {message_body}")

#         try:
#             dialog=Dialog.objects.get(id=dialog_id)
#             user = User.objects.get(id=user_id)

#             Message.objects.create(dialog_id=dialog,author_id=user,body=message_body)
#             print(f"Message_saved: {message_body}")

#         except ObjectDoesNotExist as e:
#               print(f"Error - {e}")

#         ch.basic_ack(delivery_tag=method.delivery_tag)



# def main():
#     credentials = pika.PlainCredentials(username='rmuser',password='rmpassword')
#     params=pika.ConnectionParameters(host='127.0.0.1',port='5672',credentials=credentials)
#     connection = pika.BlockingConnection(params)
#     channel=connection.channel()

#     channel.exchange_declare(exchange='dialog_exchange', exchange_type='direct', durable=True)

#     queue_name = 'general_dialog_queue'
#     channel.queue_declare(queue=queue_name)

#     def on_message_received(ch, method, properties, body):
#         # Извлекаем dialog_id из сообщения
#         message_data = json.loads(body)
#         dialog_id = message_data['dialog_id']

#         # Динамически привязываем очередь к нужному routing_key
#         routing_key = f"dialog_{dialog_id}"
#         channel.queue_bind(queue=queue_name, exchange='dialog_exchange', routing_key=routing_key)

#         # Вызываем callback для обработки сообщения
#         callback(ch, method, properties, body)

#     # channel.queue_bind(queue=queue_name, exchange='dialog_exchange', routing_key='dialog_*')

#     channel.basic_consume(queue=queue_name, on_message_callback=on_message_received, auto_ack=False)

#     print("Waiting for messages...")
#     channel.start_consuming()


# if __name__== '__main__':
#       main()