import pika
import json

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'date_me.settings')
django.setup()

from dialogs.models import Message, Dialog
from users.models import User
from django.core.exceptions import ObjectDoesNotExist




def callback(ch, method, properties, body):
        message_data = json.loads(body)
        dialog_id = message_data['dialog_id']
        user_id = message_data['user_id']
        message_body = message_data['message']
        print(f"Received message from {user_id} for dialog {dialog_id}: {message_body}")

        try:
            dialog=Dialog.objects.get(id=dialog_id)
            user = User.objects.get(id=user_id)

            Message.objects.create(dialog_id=dialog,author_id=user,body=message_body)
            print(f"Message_saved: {message_body}")

        except ObjectDoesNotExist as e:
              print(f"Error - {e}")

        ch.basic_ack(delivery_tag=method.delivery_tag)



def main():
    credentials = pika.PlainCredentials(username='rmuser',password='rmpassword')
    params=pika.ConnectionParameters(host='127.0.0.1',port='5672',credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel=connection.channel()

    channel.exchange_declare(exchange='dialog_exchange', exchange_type='direct', durable=True)

    queue_name = 'general_dialog_queue'
    channel.queue_declare(queue=queue_name)

    def on_message_received(ch, method, properties, body):
        # Извлекаем dialog_id из сообщения
        message_data = json.loads(body)
        dialog_id = message_data['dialog_id']

        # Динамически привязываем очередь к нужному routing_key
        routing_key = f"dialog_{dialog_id}"
        channel.queue_bind(queue=queue_name, exchange='dialog_exchange', routing_key=routing_key)

        # Вызываем callback для обработки сообщения
        callback(ch, method, properties, body)

    # channel.queue_bind(queue=queue_name, exchange='dialog_exchange', routing_key='dialog_*')

    channel.basic_consume(queue=queue_name, on_message_callback=on_message_received, auto_ack=False)

    print("Waiting for messages...")
    channel.start_consuming()


if __name__== '__main__':
      main()