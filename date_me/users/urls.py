from django.urls import include, path
# from users.routers import UserProfileRouter
from rest_framework import routers
from .views import RegisterOrLoginView,SelectGenderView,EnterNameSurnameView,EnterContactInfoView,UserProfileView


app_name='users'


# router=routers.SimpleRouter()
# router.register('', UserProfileView ,basename='')





urlpatterns = [
    path('',RegisterOrLoginView.as_view()),
    path('select_gender/',SelectGenderView.as_view()),
    path('enter_name_surname/',EnterNameSurnameView.as_view()),
    path('enter_contact_info/',EnterContactInfoView.as_view()),
    path('profile/',UserProfileView.as_view()),

]
