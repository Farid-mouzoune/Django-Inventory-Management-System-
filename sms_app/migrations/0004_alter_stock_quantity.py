# Generated by Django 3.2.4 on 2021-06-04 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_app', '0003_alter_stock_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]