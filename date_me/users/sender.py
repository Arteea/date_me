from django.core.mail import send_mail

from django.core.signing import TimestampSigner,SignatureExpired,BadSignature

from datetime import timedelta


from django.utils.http import urlencode
import pika
import json


from dotenv import load_dotenv
from date_me import settings
import os
load_dotenv()

def send_message(data):
    subject='Date me registration confirmation'
    email=settings.EMAIL_HOST_USER
    name=data['first_name']
    users_email=data['email']
    link=generate_link(users_email)

    message=f"Hello dear, {name}!\nCongrats for registraton on DateMe service. We hope that you will find your pair.\nPlease follow the link {link} to activate your profile"

    send_mail(      
        subject=subject,
        message=message,
        from_email=email,
        recipient_list=[users_email],
        fail_silently=False,
        )
    





signer = TimestampSigner()

def verify_token(token, max_age=timedelta(hours=24)):
    try:
        email=signer.unsign(token)
        return email
    except(BadSignature,SignatureExpired):
        return None


def generate_link(user_email):
    token=signer.sign(user_email)
    return f"http://127.0.0.1:8000/confirm_email/{token}"
    # return f"{request.scheme}://{request.get_host()}{base_url}?{query_string}"



#rabbitmq
def send_confirmation(user_data):
    try:
        credentials = pika.PlainCredentials(username=os.getenv('RABBIT_USERNAME'),password=os.getenv('RABBIT_PASSWORD'))
        params=pika.ConnectionParameters(host='127.0.0.1',port='5672',credentials=credentials)
        #Соединение с rabbitmq
        connection=pika.BlockingConnection(params)
        channel = connection.channel()
        #Объявление очереди
        channel.queue_declare(queue='email_queue', durable=True)

        #Публикуем сообщение в очередь
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=json.dumps(user_data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        print(" [x] Sent user data to RabbitMQ")
        connection.close()

    except Exception as e:
        print(f"Error sending message to RabbitMQ: {e}")




