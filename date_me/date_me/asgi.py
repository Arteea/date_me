"""
ASGI config for date_me project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from django.urls import path
from dialogs.consumers import ChatConsumer 

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from dialogs.routing import websocket_urlpatterns



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'date_me.settings')
print(os.environ["DJANGO_SETTINGS_MODULE"])
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/<str:dialog_id>/", ChatConsumer.as_asgi()),  # Обработчик для WebSocket
        ])
    ),
})

