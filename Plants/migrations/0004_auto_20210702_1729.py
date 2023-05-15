# Generated by Django 3.2.3 on 2021-07-02 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plants', '0003_plant_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_files/'),
        ),
        migrations.AddField(
            model_name='plant',
            name='plant_picture',
            field=models.ImageField(blank=True, null=True, upload_to='plant_pictures/'),
        ),
    ]
