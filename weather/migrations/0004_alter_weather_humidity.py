# Generated by Django 4.2.4 on 2023-08-20 18:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('weather', '0003_weather_image_alter_weather_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='humidity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
