# Generated by Django 2.1.3 on 2018-11-16 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20181116_1655'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userlike',
            unique_together={('from_user', 'to_user')},
        ),
    ]
