# Generated by Django 2.1.5 on 2019-01-20 09:13

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_staticcontent_index_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticcontent',
            name='index_mobile_html',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='모바일 HTML'),
        ),
    ]