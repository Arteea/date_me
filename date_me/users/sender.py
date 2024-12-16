from django.core.mail import send_mail


from django.core.signing import TimestampSigner,SignatureExpired,BadSignature

from datetime import timedelta


from django.utils.http import urlencode

def send_message(data):
    subject='Date me registration confirmation'
    email='artea777@rambler.ru'
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

def generate_token(user_email):
    return signer.sign(user_email)


def verify_token(token, max_age=timedelta(hours=24)):
    try:
        email=signer.unsign(token)
        return email
    except(BadSignature,SignatureExpired):
        return None


def generate_link(user_email):
    token=generate_token(user_email)
    return f"http://127.0.0.1:8000/confirm_email/{token}"
    # return f"{request.scheme}://{request.get_host()}{base_url}?{query_string}"



    



