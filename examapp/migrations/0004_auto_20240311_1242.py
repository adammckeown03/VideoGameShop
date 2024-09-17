# Generated by Django 3.2.12 on 2024-03-11 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0003_game_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='quantity',
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examapp.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='users_basket',
            field=models.ManyToManyField(blank=True, related_name='basket', through='examapp.BasketItem', to=settings.AUTH_USER_MODEL),
        ),
    ]
