from django.core.signing import BadSignature, SignatureExpired

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserInfoSerializer,ButtonActionSerializer,NameSurnameSerializer,GenderSerializer,ContactInfoSerializer

from users.models import User,UserInfo

from .sender import send_message, verify_token,send_confirmation

from zodiac.utils import get_zodiac_id






class UserProfileView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    ###Метод для получения объекта данных информации о пользователе
    def get_userinfo(self):
        try:
            return UserInfo.objects.filter(user=self.request.user)
        except UserInfo.DoesNotExist:
            raise Response({'error': 'User data not found'}, status=status.HTTP_404_NOT_FOUND)



    def get(self, request, *args, **kwargs):
        ###Получаем данные пользователя
        user_info=self.get_userinfo()
        serializer = self.serializer_class(user_info,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
    
    def put(self,request,*args,**kwargs):
        updated_data=request.data  ###Обновленные данные c фронтенда
        old_user_info=self.get_userinfo()
        serializer = UserInfoSerializer(old_user_info, data=updated_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def delete(self,request,*args,**kwargs):
        user=request.user
        user.delete()
        return Response({'message': 'User and related data successfully deleted'}, status=status.HTTP_204_NO_CONTENT)




    





class RegisterOrLoginView(APIView):

    serializer_class=ButtonActionSerializer

    def post(self,request):
        action=request.data.get('action')
        if action=='signup':
            redirect_url = "http://127.0.0.1:3000/select_gender"
        elif action=='login':
            redirect_url="http://127.0.0.1:3000/api/token/"
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "success","redirect_url" : redirect_url}, status=status.HTTP_200_OK) 






class SelectGenderView(APIView):

    serializer_class=GenderSerializer

    def post(self,request,*args,**kwargs):
        redirect_url='http://127.0.0.1:3000/enter_name_surname/'
        gender=request.data.get('gender')
        birth_date=request.data.get('birth_date')
        user_info_data={'gender':gender,'birth_date':birth_date}     #dict for later creating UserInfo object
        
        serializer=GenderSerializer(data=user_info_data)
        
        if serializer.is_valid():
            user_info_data['zodiac_id']=get_zodiac_id(birth_date,gender)  #determination zodiac sign for user according to his birth date 
            return Response({"redirect_url" : redirect_url,'user_info':user_info_data}, status=status.HTTP_200_OK)
        else:
            return Response(f"Ошибка валидации {serializer.errors}",status=status.HTTP_400_BAD_REQUEST)






class EnterNameSurnameView(APIView):

    serializer_class=NameSurnameSerializer
        
    def post(self,request,*args,**kwargs):
        redirect_url='http://127.0.0.1:3000/enter_contact_info/'
        user_data={}
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        user_data["first_name"]=first_name
        user_data["last_name"]=last_name

        serializer=NameSurnameSerializer(data=user_data)

        if serializer.is_valid():
            request.data["user_data"]=user_data
            return Response({'redirect_url':redirect_url, "user_data":serializer.validated_data})
        else:
            return Response(f"Ошибка валидации {serializer.errors}",status=status.HTTP_200_OK)

        
    




class EnterContactInfoView(APIView):

    serializer_class=ContactInfoSerializer

    def post(self,request,*args,**kwargs):

        user_credentials=request.data
        user_info_data = user_credentials.pop('user_data') ###Data about user from previous pages
        
        redirect_url='http://127.0.0.1:3000/api/token/'

        user_name_data={'first_name':user_info_data.pop('first_name'),'last_name':user_info_data.pop('last_name')}
        serializer=ContactInfoSerializer(data=user_credentials)

        if serializer.is_valid():
            ###Creation new User object
            user_data=serializer.data
            user_data.update(user_name_data)
            new_user=User.objects.create(**user_data)
 
            send_confirmation(user_data) ###Email confirmation via rabbitmq

            ###Creation new UserInfo object
            user_id=User.objects.filter(email=new_user.email).first().id
            user_info_data['user_id'] = user_id
            new_user_info=UserInfo.objects.create(**user_info_data)
            return Response({'redirect_url':redirect_url},status=status.HTTP_200_OK)          
        else:
            return Response(f"Ошибка валидации {serializer.errors}",status=status.HTTP_400_BAD_REQUEST)





class ConfirmEmailView(APIView):

    def get(self,request,*args,**kwargs):
        token = request.query_params.get('token')
        print(f"TOKEN_____{token}")
        if not token:
            return Response({"error": "Токен не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            email=verify_token(token)
            User.objects.filter(email=email).update(is_verified=True)
            return Response({"detail": "Email успешно подтвержден!"}, status=status.HTTP_200_OK)
        except SignatureExpired:
            return Response({"error": "Токен устарел"}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({"error": "Неверный токен"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)



        
        
        
        
            
          
            





