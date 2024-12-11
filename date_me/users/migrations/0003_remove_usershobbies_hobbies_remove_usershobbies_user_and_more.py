# Generated by Django 5.1.3 on 2024-11-18 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_name_remove_user_surname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usershobbies',
            name='hobbies',
        ),
        migrations.RemoveField(
            model_name='usershobbies',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='users_hobbies',
        ),
        migrations.RenameField(
            model_name='usersmedia',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='zodiac_id',
        ),
        migrations.RemoveField(
            model_name='usersmedia',
            name='media_url_list',
        ),
        migrations.AddField(
            model_name='usersmedia',
            name='media_url',
            field=models.URLField(default=None, verbose_name='Ссылка на медиа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.DeleteModel(
            name='Hobby',
        ),
        migrations.DeleteModel(
            name='UsersHobbies',
        ),
    ]
