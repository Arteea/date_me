from rest_framework import serializers
from .models import User, UserInfo
import re
from datetime import date


from django.contrib.auth.hashers import make_password


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



class ButtonActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["login", "signup"])


class GenderSerializer(serializers.Serializer):

    gender = serializers.ChoiceField(choices=["male", "female"])
    birth_date = serializers.DateField()

    def validate_birth_date(self,birth_date):
        if not birth_date:
            raise serializers.ValidationError('Поле "Дата рождения" не должно быть пустым')
        elif date.today()<birth_date:
            raise serializers.ValidationError('Дата рождения не может быть в будущем')
        today=date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age<18:
            raise serializers.ValidationError('Возраст должен быть не менее 18 лет')
        return birth_date



class NameSurnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
    
    def validate_first_name(self,first_name):
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ]+$',first_name):
            raise serializers.ValidationError('Некорректное имя пользователя,имя не должно содержать цифры и спецсимволы')
        return first_name

    def validate_last_name(self,last_name):
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ]+$',last_name):
            raise serializers.ValidationError('Некорректная фамилия пользователя,фамилия не должна содержать цифры и спецсимволы')
        return last_name
    





class ContactInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['email', 'username','phone_number','password']
        
        
        def validate_phone_number(self, phone_number):
            if not re.match(r'^\+7\d{10}$', phone_number):
                raise serializers.ValidationError('Номер телефона должен быть в формате +7XXXXXXXXXX')
            if User.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError('Пользователь с таким номером телефона уже существует')
            return phone_number
        
        def validate_email(self,email):
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',email):
                raise serializers.ValidationError('Неверный формат email адреса')
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError('Пользователь с таким email уже зарегестрирован')
            return email

        def validate_username(self,username):
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError('Пользователь с таким username уже зарегестрирован')
            return username
        
        # def validate_password(self,password):
        #     if not re.match(r'^(?:[a-zA-Z]+|\d+|[!@#$%^&*()_+=-]+|.{0,7})$',password):
        #         raise serializers.ValidationError('Пароль слишком слабый') 
        #     return password


        


