# Generated by Django 2.1.3 on 2018-12-03 13:22

import colorful.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_auto_20181129_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticcontent',
            name='index_mobile_color',
            field=colorful.fields.RGBColorField(blank=True, verbose_name='메인페이지 모바일 배경색'),
        ),
        migrations.AddField(
            model_name='staticcontent',
            name='index_mobile_image',
            field=models.ImageField(blank=True, help_text='모바일 이미지는 가로를 가득 채우도록 설정됩니다', upload_to='index', verbose_name='메인페이지 모바일 이미지'),
        ),
        migrations.AlterField(
            model_name='staticcontent',
            name='company_list_image',
            field=models.ImageField(blank=True, help_text='참여기업 목록의 배너 이미지 입니다.', upload_to='static', verbose_name='참여기업 목록 이미지'),
        ),
        migrations.AlterField(
            model_name='staticcontent',
            name='index_color',
            field=colorful.fields.RGBColorField(blank=True, help_text='배너 이미지의 남는 공간을 채울 배경색입니다.', verbose_name='메인페이지 배경색'),
        ),
        migrations.AlterField(
            model_name='staticcontent',
            name='index_height',
            field=models.IntegerField(default=200, help_text='메인 배너 이미지의 세로 길이를 지정합니다. 가로길이는 세로 길이의 비율로 정해집니다.', verbose_name='메인페이지 이미지 세로 길이(px)'),
        ),
    ]
