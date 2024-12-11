from django import forms
from users.models import User, UserInfo
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm



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
    
    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # email = forms.EmailField()
    phone_number = forms.CharField(required=True)
    # password1 = forms.CharField()
    # password2 = forms.CharField()


class ProfileUserForm(UserChangeForm):
    class Meta:
        model = UserInfo
        fields = (
            "user",
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


# class UserLoginForm(AuthenticationForm):

#     username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    
#     def clean_username(self):
#         # Переопределяем метод clean для поля username, чтобы он работал с email
#         email = self.cleaned_data.get('username')
        
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise forms.ValidationError('Пользователь с таким email не существует.')
        
#         # Возвращаем email, но в действительности это будет email пользователя, с которым происходит аутентификация
#         return user.username

#     class Meta:
#         model = User
#         fields = ['email', 'password']
