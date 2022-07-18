# Generated by Django 4.0.6 on 2022-07-17 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AH_Dump',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_url', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='AH_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_id', models.CharField(max_length=50, unique=True)),
                ('item_id', models.CharField(max_length=50)),
                ('item', models.CharField(max_length=500)),
                ('bid', models.CharField(max_length=50)),
                ('buyout', models.CharField(max_length=50)),
                ('quantity', models.CharField(max_length=50)),
                ('time_left', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ah', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ah_dump')),
            ],
        ),
    ]
