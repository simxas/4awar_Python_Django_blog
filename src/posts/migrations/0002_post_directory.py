# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-12 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='directory',
            field=models.CharField(max_length=120, null=True),
        ),
    ]