# Generated by Django 3.2.4 on 2021-06-08 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_app', '0018_alter_stock_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='reorder_level',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
