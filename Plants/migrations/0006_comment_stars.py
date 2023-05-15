# Generated by Django 3.2.3 on 2021-07-02 19:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plants', '0005_remove_plant_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='stars',
            field=models.IntegerField(default=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
