# Generated by Django 2.1.3 on 2018-11-16 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_user_is_looking'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_publish',
            field=models.BooleanField(default=False, verbose_name='이력서 공개여부'),
        ),
    ]
