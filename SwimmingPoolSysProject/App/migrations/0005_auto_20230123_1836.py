# Generated by Django 3.0.14 on 2023-01-23 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_ticket_dateofpurchase_complaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='dateOfPurchase',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 23, 18, 36, 44, 485325)),
        ),
    ]
