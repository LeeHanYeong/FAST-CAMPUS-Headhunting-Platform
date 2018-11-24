# Generated by Django 2.1.3 on 2018-11-24 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20181124_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_looking',
            field=models.CharField(choices=[('n', '신입'), ('e', '경력'), ('s', '커리어 전환'), ('c', '구직 완료')], default='s', max_length=1, verbose_name='지원자 상태'),
        ),
    ]