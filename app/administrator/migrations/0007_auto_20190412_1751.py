# Generated by Django 2.1.7 on 2019-04-12 08:51
from django.contrib.sites.models import Site
from django.db import migrations


def forward_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Site.objects.using(db_alias).update_or_create(
        pk=1,
        defaults={
            'domain': 'link.fastcampus.co.kr',
            'name': 'link.fastcampus.co.kr',
        }
    )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('administrator', '0006_auto_20190223_1805'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func),
    ]