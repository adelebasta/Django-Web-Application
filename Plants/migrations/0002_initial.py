# Generated by Django 3.2.3 on 2021-06-15 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Plants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='myuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vote',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Plants.plant'),
        ),
        migrations.AddField(
            model_name='plant',
            name='myuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myusers', related_query_name='myuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='myuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Plants.plant'),
        ),
    ]