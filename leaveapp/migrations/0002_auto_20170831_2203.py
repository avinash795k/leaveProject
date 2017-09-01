# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveremaining',
            name='leaveremaining_VL',
            field=models.IntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='leaveremaining',
            name='leaveremaining_CL',
            field=models.IntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='leaveremaining',
            name='leaveremaining_COL',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='leaveremaining',
            name='leaveremaining_EL',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='leaveremaining',
            name='leaveremaining_RH',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='leaveremaining',
            name='leaveremaining_SCL',
            field=models.IntegerField(default=15),
        ),
    ]
