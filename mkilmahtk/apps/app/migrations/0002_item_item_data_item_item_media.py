# Generated by Django 4.0.6 on 2022-07-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_data',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='item',
            name='item_media',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
