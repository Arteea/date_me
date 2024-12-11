from django.urls import include, path
# from users.routers import UserProfileRouter
from rest_framework import routers
from .views import UserProfileView,UserRegistrationView


app_name='users'


# router=routers.SimpleRouter()
# router.register('', UserProfileView ,basename='')





urlpatterns = [
    path('registration/',UserRegistrationView.as_view()),
]
