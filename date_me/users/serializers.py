from rest_framework import serializers
from .models import User, UserInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','phone_number','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user=User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password']) #хеширование пароля для корректной аутентификации пользователя
        user.save()
        return user

class UserInfoSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserInfo
        fields = '__all__'