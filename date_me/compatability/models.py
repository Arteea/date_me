from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from zodiac.models import Zodiac
from users.models import User


class Compatability(models.Model):
    zodiac_female = models.ForeignKey(to=Zodiac, on_delete=models.CASCADE,related_name='compatability_from',verbose_name='Совместимость знака зодиака')
    zodiac_male = models.ForeignKey(to=Zodiac, on_delete=models.CASCADE,related_name='compatability_to',verbose_name='К знаку зодиака')
    compatability = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)], verbose_name='Уровень совместимости')


    def __str__(self):
        return f"{self.zodiac_female.name}  → {self.zodiac_male.name} : {self.compatibility}%"

    class Meta:
        verbose_name = "Совместимость"
        verbose_name_plural = "Совместимости"
        unique_together = ("zodiac_female", "zodiac_male")


class Swipes(models.Model):
    swiper_id = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='swiped_by',verbose_name='Свайпер')
    candidate_id=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='candidate',verbose_name='Кандидат')
    action = models.BooleanField(verbose_name='Значение свайпа')
    timestamp= models.DateTimeField(auto_now_add=True,verbose_name='Время свайпа')

    def __str__(self):
        return f"{self.swiper_id.username}  свайпнул {self.candidate_id.username} : {['влево','вправо'][self.action]}"