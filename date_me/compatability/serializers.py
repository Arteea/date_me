from rest_framework import serializers
from .models import Swipes
from users.models import UserInfo


class SwipeActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["Yes", "No"])



class CandidateSerializer(serializers.Serializer):
    zodiac_name = serializers.CharField(source='zodiac.name', read_only=True)
    class Meta:
        model = UserInfo
        fields = ['description', 'zodiac_name']