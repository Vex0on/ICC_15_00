# Generated by Django 3.0.14 on 2023-01-23 19:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_auto_20230123_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='dateOfPurchase',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 23, 20, 14, 42, 45490), editable=False),
        ),
    ]
