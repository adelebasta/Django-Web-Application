# Generated by Django 3.2.3 on 2021-06-28 17:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Useradmin', '0002_alter_myuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2001, 6, 28)),
        ),
    ]