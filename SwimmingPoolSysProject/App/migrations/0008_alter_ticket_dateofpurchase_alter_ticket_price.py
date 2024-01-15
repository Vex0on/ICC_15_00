# Generated by Django 4.2 on 2023-04-16 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_client_user_alter_ticket_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='dateOfPurchase',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 16, 20, 1, 50, 959000)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.CharField(choices=[('19.99', '19.99zł - ulgowy'), ('25', '25zł - normalny'), ('33', '33zł - grupowy')], default=('25', '25zł - normalny'), max_length=6),
        ),
    ]