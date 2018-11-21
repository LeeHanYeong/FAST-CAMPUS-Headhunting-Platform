# Generated by Django 2.1.3 on 2018-11-21 16:56

import colorful.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_auto_20181122_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticcontent',
            name='index_color',
            field=colorful.fields.RGBColorField(blank=True, verbose_name='메인페이지 배경색'),
        ),
        migrations.AddField(
            model_name='staticcontent',
            name='index_image',
            field=models.ImageField(blank=True, upload_to='index', verbose_name='메인페이지 이미지'),
        ),
    ]
