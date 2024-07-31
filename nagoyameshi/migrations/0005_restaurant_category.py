# Generated by Django 4.2.11 on 2024-07-30 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nagoyameshi', '0004_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='nagoyameshi.category'),
            preserve_default=False,
        ),
    ]
