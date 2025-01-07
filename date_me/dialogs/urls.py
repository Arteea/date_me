from django.urls import path
from . import views


app_name='chat'


urlpatterns = [
    path('chat/<int:dialog_id>/', views.chat_room, name='chat_room'),  # URL для страницы чата с динамическим dialog_id
]