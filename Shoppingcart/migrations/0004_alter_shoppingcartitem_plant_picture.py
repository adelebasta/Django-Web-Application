# Generated by Django 3.2.3 on 2021-07-06 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shoppingcart', '0003_alter_shoppingcartitem_plant_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcartitem',
            name='plant_picture',
            field=models.ImageField(blank=True, default='../../media/plant_pictures/default_sc.jpg', null=True, upload_to='plant_pictures/'),
        ),
    ]
