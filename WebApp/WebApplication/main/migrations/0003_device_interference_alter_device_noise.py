# Generated by Django 4.2.1 on 2023-05-25 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_decision_time_remove_device_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='interference',
            field=models.FloatField(default=0, max_length=250, verbose_name='Уровень помех в сети (дБ)'),
        ),
        migrations.AlterField(
            model_name='device',
            name='noise',
            field=models.FloatField(max_length=250, verbose_name='Уровень шума в сети (дБ)'),
        ),
    ]
