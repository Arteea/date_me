# Generated by Django 5.1.3 on 2024-12-27 22:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_userinfo_compatability_preferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='compatability_preferences',
            field=models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
