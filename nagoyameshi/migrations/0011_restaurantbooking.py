# Generated by Django 4.2.11 on 2024-09-23 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nagoyameshi', '0010_remove_favoriterestaurant_favorite_restaurant_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='作成日時')),
                ('start', models.DateTimeField(verbose_name='開始時間')),
                ('end', models.DateTimeField(verbose_name='終了時間')),
                ('people_number', models.IntegerField(verbose_name='予約人数')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nagoyameshi.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
