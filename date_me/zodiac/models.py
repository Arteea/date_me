from django.db import models

class Zodiac(models.Model):
    name = models.CharField(max_length=50,blank=False,verbose_name='Знак зодиака')
    gender = models.CharField(max_length=6,choices=[('male', 'мужчина'), ('female', 'женщина')],default="male",verbose_name='Пол')
    description = models.TextField(max_length=350,verbose_name='Описание знака зодиака')
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Знак зодиака"
        verbose_name_plural = 'Знаки зодиака'