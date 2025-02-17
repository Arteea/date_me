# Generated by Django 5.1.3 on 2024-12-26 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_userinfo_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='birth_place',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Место рождения'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='birth_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время рождения'),
        ),
    ]
