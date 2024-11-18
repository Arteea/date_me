from django.urls import path

from users import views

app_name='users'

urlpatterns = [
    path('registration/',views.UserRegistrationView.as_view(), name='registration'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
]
