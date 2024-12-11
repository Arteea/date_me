from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
from .serializers import UserSerializer,UserInfoSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .permissions import IsAuthenticatedAndOwner
from rest_framework import permissions
from rest_framework.decorators import action


class UserRegistrationView(CreateAPIView):
    serializer_class=UserSerializer

    def get(self,request,*args,**kwargs):
        serializer=self.get_serializer()
        return Response(serializer.data)




class UserProfileView(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,GenericViewSet):
        # queryset = UserInfo.objects.all()
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
                # if getattr(profile, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                    # profile._prefetched_objects_cache = {}
                # data=serializer.data
                # data['message']='Профиль обновлен'
                # print(data)
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
        
        
        
        
            
            
            





