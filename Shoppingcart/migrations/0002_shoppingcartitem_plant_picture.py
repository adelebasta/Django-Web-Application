# Generated by Django 3.2.3 on 2021-07-06 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shoppingcart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartitem',
            name='plant_picture',
            field=models.ImageField(blank=True, default='plant_pictures/default_sc.jpg', null=True, upload_to='plant_pictures/'),
        ),
    ]
