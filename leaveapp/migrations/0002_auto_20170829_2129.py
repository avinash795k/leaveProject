# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='station_add',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
