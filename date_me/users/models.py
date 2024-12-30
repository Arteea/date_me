from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.validators import RegexValidator,MaxValueValidator,MinValueValidator
#from django.contrib.gis.db import models
from zodiac.models import Zodiac

class User(AbstractUser):
    username = models.CharField(default='user',max_length=50,unique=True,blank=False)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=150,blank=False)
    email = models.EmailField(unique=True,blank=False)
    phone_number = models.CharField(max_length=12,blank=True,null=True,unique=True,validators=[RegexValidator(regex=r'^\+7\d{10}$', message="Формат: '+7XXXXXXXXXX'.")])
    password=models.CharField(max_length=128,blank=False)
    is_verified=models.BooleanField(default=False)

    class Meta:
        db_table='user'
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f'Пользователь {self.first_name} {self.last_name}'


class UsersMedia(models.Model):
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE, verbose_name='Пользователь')
    media_url = models.URLField(verbose_name='Ссылка на медиа')

    class Meta:
        db_table='usersmedia'
        verbose_name = "Медиа пользователя"
        verbose_name_plural = 'Медиа пользователей'
    
    def __str__(self):
        return f'Медиа пользователя  {self.user.id} - {self.user.name} {self.user.surname}'






class UserInfo(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE,verbose_name='Пользователь',related_name='info')
    description = models.TextField(max_length=350,blank=True,verbose_name='Описание')
    birth_date = models.DateField(verbose_name="Дата рождения")
    birth_place = models.CharField(blank=True,max_length=100,verbose_name='Место рождения',null=True)
    birth_time = models.TimeField(blank=True,verbose_name='Время рождения',null=True)
    height = models.IntegerField(blank=True,verbose_name='Рост',null=True)
    gender = models.CharField(max_length=6,choices=[('male', 'Мужской'), ('female', 'Женский')],verbose_name='Пол')
    zodiac = models.ForeignKey(to=Zodiac,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Знак зодиака')
    compatability_preferences = models.IntegerField(default=50,validators=[MinValueValidator(50),MaxValueValidator(100)])
    #location = models.PointField(blank=True,verbose_name='Географическая точка')


    class Meta:
        db_table = 'userinfo'
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'
        
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    

