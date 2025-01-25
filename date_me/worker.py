import os
import django
import pika
import json

from django.core.mail import send_mail
from django.core.signing import TimestampSigner,SignatureExpired,BadSignature
from datetime import timedelta




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'date_me.settings')
django.setup()



def send_message(data):
    subject='Date me registration confirmation'
    email=os.getenv('EMAIL_HOST_USER')
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


def generate_link(user_email):
    token=signer.sign(user_email)
    return f"http://127.0.0.1:3000/confirm_email/?token={token}"
    # return f"{request.scheme}://{request.get_host()}{base_url}?{query_string}"




#worker RabbitMQ
def callback(channel,method,properties,body):
    print(" [x] Recieved message")
    user_data = json.loads(body)
    try:
        send_message(user_data)
        print(f" [x] Email sent to {user_data['email']}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Failed to send email: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag)



def main():

    #Connection to RabbitMQ
    credentials = pika.PlainCredentials(username='rmuser',password='rmpassword')
    params=pika.ConnectionParameters(host='127.0.0.1',port='5672',credentials=credentials)
    connection=pika.BlockingConnection(params)
    channel =connection.channel()

    #Queue announcement
    channel.queue_declare(queue='email_queue', durable=True)

    #Queue subscription
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    print('[*] Waiting for messages.')
    channel.start_consuming()


if __name__ == "__main__":
    main()
