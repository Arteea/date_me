import json
from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer

def chat_room(request, dialog_id):
    previous_messages=Message.objects.filter(dialog_id=dialog_id).order_by('-timestamp')[:20]
    previous_messages=reversed(previous_messages)
    serialized_messages=MessageSerializer(previous_messages,many=True).data
    serialized_messages=json.dumps(serialized_messages)
    return render(request, 'chat.html', {'dialog_id': dialog_id,'user_id': request.user.id,'previous_messages':serialized_messages, })

