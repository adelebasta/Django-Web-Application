# Generated by Django 3.2.3 on 2021-07-08 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Plants', '0012_plant_avg_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='avg_rating',
        ),
    ]
