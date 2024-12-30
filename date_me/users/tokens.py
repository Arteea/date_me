from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect

from django.contrib.auth import login
from .models import UserInfo

import jwt
from date_me.settings import SECRET_KEY,SIMPLE_JWT


from django.contrib.auth import get_user_model # Для исключения ошибки при использовании кастомной модели пользователя для аутентификации пользователя
User = get_user_model()                        #

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    print("CustomTokenObtainPairView: CustomTokenObtainPairView called")

    def post(self, request, *args, **kwargs):


        response=super().post(request, *args, **kwargs)
        
        if response.status_code==200:
        
            access_token = response.data.get('access')

            if access_token:
                try:
                    decoded_token=jwt.decode(access_token, SECRET_KEY, algorithms=[SIMPLE_JWT.get('ALGORITHM')])       
                    user_id = decoded_token.get('user_id')
                    user= User.objects.get(id=user_id)
                    login(request, user)
                    request.session['user_id']=user_id
                    response.data['user_id']=user_id

                except jwt.ExpiredSignatureError:
                    return Response({"error": "Token expired"}, status=status.HTTP_400_BAD_REQUEST)
                

                except jwt.InvalidTokenError:
                    return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
                

            user_info=UserInfo.objects.filter(user_id=user_id).first()
            user=User.objects.get(id=user_id)


            if user_info:
                redirect_url = f'accounts/profile/{user_id}'
            else:
                redirect_url = 'accounts/create_profile/'

            response.data['redirect_url'] = redirect_url
            # return response
            return redirect(redirect_url,user_id=user_id)
        return response


            
