# Generated by Django 2.1.3 on 2018-11-15 05:12

from django.db import migrations
import django_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img_profile',
            field=django_fields.fields.DefaultStaticImageField(blank=True, upload_to='user', verbose_name='프로필 이미지'),
        ),
    ]
