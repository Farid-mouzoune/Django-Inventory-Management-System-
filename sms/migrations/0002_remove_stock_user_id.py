# Generated by Django 3.2.4 on 2021-06-04 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='user_id',
        ),
    ]
