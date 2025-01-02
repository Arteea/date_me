from django.db import models
from users.models import User

class Pair(models.Model):
    first_participant = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='pairs_as_first',verbose_name='Первый участник пары')
    second_participant = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='pairs_as_second',verbose_name='Второй участник пары')
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name='Время создания пары')

    def save(self,*args,**kwargs):
        ###Check if Pair object is newly created(doesn't have pk)
        is_new = self.pk is None
        super().save(*args,**kwargs)
        if is_new:
            Dialog.objects.create(pair=self)




class Dialog(models.Model):
    pair= models.OneToOneField(to=Pair, on_delete=models.CASCADE, null=False, blank=False, related_name="dialog", verbose_name="Пара")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Время создания диалога')


    def get_participants(self):
        return [self.pair.first_participant, self.pair.second_participant]
    



class Message(models.Model):
    dialog_id = models.ForeignKey(to=Dialog, on_delete=models.CASCADE,related_name="message", verbose_name='Сообщение')
    author_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="message_author",verbose_name='Автор сообщения')
    body = models.TextField(max_length=350,verbose_name="Тело сообщения")
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name='Время создания сообщения')