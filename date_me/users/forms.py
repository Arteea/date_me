from django import forms
from users.models import User, UserInfo
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class RegistrationUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
            "password2",
        )
    
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class ProfileUserForm(UserChangeForm):
    class Meta:
        model = UserInfo
        fields = (
            "sex",
            "description",
            "height",
            "birth_date",
            "birth_place",
            "birth_time",
        )
    
    sex = forms.BooleanField()
    description = forms.Textarea()
    height = forms.IntegerField()
    birth_date = forms.DateField()
    birth_place = forms.CharField()
    birth_time = forms.TimeField()