# Generated by Django 4.2.11 on 2024-07-30 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nagoyameshi', '0008_alter_restaurant_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nagoyameshi.category'),
        ),
    ]
