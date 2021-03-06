# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-14 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wallpapers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryToWallpaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallpapers.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Wallpaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=wallpapers.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(blank=True, default=0, null=True)),
                ('width_field', models.IntegerField(blank=True, default=0, null=True)),
                ('directory', models.CharField(max_length=120, null=True)),
                ('description', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(blank=True, null=True, through='wallpapers.CategoryToWallpaper', to='wallpapers.Category')),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
                'verbose_name_plural': 'Wallpapers',
            },
        ),
        migrations.AddField(
            model_name='categorytowallpaper',
            name='wallpaper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallpapers.Wallpaper'),
        ),
    ]
