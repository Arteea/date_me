from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    
    author_name = serializers.CharField(source = 'author_id.first_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'author_name', 'body', 'timestamp']