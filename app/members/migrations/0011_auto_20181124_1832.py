# Generated by Django 2.1.3 on 2018-11-24 09:32

from django.db import migrations
import django_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_user__company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='career',
            name='content',
        ),
        migrations.AlterField(
            model_name='link',
            name='img_icon',
            field=django_fields.fields.DefaultStaticImageField(blank=True, upload_to='link', verbose_name='아이콘'),
        ),
    ]