from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect

from django.contrib.auth.models import User
from .models import UserInfo

import jwt
from date_me.settings import SECRET_KEY,SIMPLE_JWT

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    print("CustomTokenObtainPairView: CustomTokenObtainPairView called")

    def post(self, request, *args, **kwargs):

        print("CustomTokenObtainPairView: POST method called")

        response=super().post(request, *args, **kwargs)

        print(response.data)
        print(request.user.id)
        
        if response.status_code==200:
        
            print("Response status is 200")
            access_token = response.data.get('access')
            print(f'accesss_token:{access_token}')

            if access_token:
                try:
                    decoded_token=jwt.decode(access_token, SECRET_KEY, algorithms=[SIMPLE_JWT.get('ALGORITHM')])
                    print(decoded_token)  
        
                    user_id = decoded_token.get('user_id')  # Или используйте нужный ключ, в зависимости от того, как вы строите токен
                    print(f"user_id: {user_id}")
                    response.data['user_id']=user_id

                except jwt.ExpiredSignatureError:
                    return Response({"error": "Token expired"}, status=status.HTTP_400_BAD_REQUEST)
                

                except jwt.InvalidTokenError:
                    return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
                

            user_info=UserInfo.objects.filter(user_id=user_id).first()  
            if user_info:
                redirect_url = f'accounts/profile/{user_id}'
            else:
                redirect_url = 'accounts/create_profile/'

            data=response.data
            data['redirect_url'] = redirect_url
            print(redirect_url)
            return redirect(redirect_url,user_id=user_id)
        return response


            
