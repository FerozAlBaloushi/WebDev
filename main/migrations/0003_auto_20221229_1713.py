# Generated by Django 2.2.8 on 2022-12-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_music_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='averageRating',
            field=models.FloatField(default=0),
        ),
    ]
