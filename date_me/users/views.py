from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from django.contrib.auth.views import LoginView
from users.models import User,UserInfo
from .forms import ProfileUserForm, RegistrationUserForm
from django.contrib import auth


# from rest_framework import generics
from rest_framework import viewsets,mixins,status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer,UserInfoSerializer,ButtonActionSerializer,NameSurnameSerializer,GenderSerializer,ContactInfoSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .permissions import IsAuthenticatedAndOwner
from rest_framework import permissions
from rest_framework.decorators import action



from django.contrib.auth.hashers import make_password



from django.core.mail import send_mail


from .sender import send_message, verify_token


class UserRegistrationView(CreateAPIView):
    serializer_class=UserSerializer

    def get(self,request,*args,**kwargs):
        serializer=self.get_serializer()
        return Response(serializer.data)




class UserProfileView(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,GenericViewSet):
        serializer_class=UserInfoSerializer
        # permission_classes=(IsAuthenticatedAndOwner, )
        
        def get_queryset(self):
            return UserInfo.objects.filter(user=self.request.user)


        @action(detail=True, methods=['get','put'], url_path='profile')
        def profile(self,request,user_id,*args,**kwargs):
            # user=response.data['user_id']
            print('Запуск профиля')
            # profile = UserInfo.objects.all.get(user_id=user)
            
            if request.method=='GET':
                profile =UserInfoSerializer(UserInfo.objects.filter(user_id=user_id).first())
                if profile:
                    return Response(profile.data,status=status.HTTP_200_OK)
                return Response({'error':'Профиль не найден'},status=status.HTTP_404_NOT_FOUND)
            
            elif request.method=="PUT":
                
                profile=UserInfo.objects.filter(user_id=user_id).first()
                
                partial = kwargs.pop('partial', True)

                print(f'update_profile:{user_id}')

                serializer = self.get_serializer(profile, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
            
                print(f"Serializer - {serializer}")
                super().perform_update(serializer)

                return Response(serializer.data,status=status.HTTP_200_OK)

            

        
        
        @action(detail=False,methods=['post'],url_path='create_profile')
        def create_profile(self, request, *args, **kwargs):
            user=request.user.id
            if UserInfo.objects.filter(user_id=user).exists():
                return Response({'error':'Профиль уже существует'},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        



class RegisterOrLoginView(APIView):

    serializer_class=ButtonActionSerializer

    def post(self,request):
        action=request.data.get('action')
        if action=='signup':
            return redirect("select_gender/", status=status.HTTP_200_OK)  #"registration/"
        elif action=='login':
            return redirect("api/token/", status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)




class SelectGenderView(GenericViewSet):

    serializer_class=GenderSerializer

    @action(detail=False,method=['post'],url_path='select_gender')
    def select_gender(self,request):
        gender=request.data.get('gender')
        redirect_url='/enter_name_surname/'
        user_info_data={'sex':gender}
        request.session["user_info_data"]=user_info_data
        print(f'data-{gender}')
        return redirect(redirect_url)
    


class EnterNameSurnameView(GenericViewSet):

    serializer_class=NameSurnameSerializer
        
    @action(detail=False,method=["post"],url_path='enter_name_surname')
    def enter_name_surname(self,request,*args,**kwargs):
        redirect_url='/enter_contact_info/'
        user_data={}
        print(f'DATA-{user_data}')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        user_data["first_name"]=first_name
        user_data["last_name"]=last_name

        serializer=NameSurnameSerializer(data=user_data)

        if serializer.is_valid():
            request.session["user_data"]=user_data
            return redirect(redirect_url)
        else:
            return Response(f"Ошибка валидации {serializer.errors}",status=status.HTTP_200_OK)

        
    




class EnterContactInfoView(GenericViewSet):

    serializer_class=ContactInfoSerializer

    @action(detail=False,method=["post"],url_path='enter_contact_info')
    def enter_contact_info(self,request,*args,**kwargs):

        name_data=request.session.get('user_data')        #First_name,last_name data for future User.object creation
        user_data={}                                      #Dict for later gathering of all user's data for User.object creation 
        user_info=request.data.items()
        
        for key,value in user_info:
            if key=='csrfmiddlewaretoken':
                pass
            elif key=='password':
                user_data[key]=make_password(value)
            else:
                user_data[key]=value

        serializer=ContactInfoSerializer(data=user_data)

        if serializer.is_valid():
            user_data.update(name_data)
            # return Response(f"User_data-{user_data}")
            send_message(user_data)
            new_user=User(**user_data)
            new_user.save()
            # return redirect('/api/token/',status=status.HTTP_200_OK)
            return Response(f'mail on {user_data["email"]} was sent',status=status.HTTP_200_OK)            
        else:
            return Response(f"Ошибка валидации {serializer.errors}",status=status.HTTP_400_BAD_REQUEST)




class ConfirmEmailView(APIView):

    def get(request,*args,token,**kwargs):
        print(f'TOKEN-------{token}')
        email=verify_token(token)

        if email:
            User.objects.filter(email=email).update(is_verified=True)
            return Response({"detail": "Email успешно подтвержден!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Ссылка недействительна или истек срок действия токена."}, status=status.HTTP_400_BAD_REQUEST)



        
        
        
        
            
          
            





