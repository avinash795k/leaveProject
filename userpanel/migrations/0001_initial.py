# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 17:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAllpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpanel.AllPost')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeaveauthority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authority_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeaveseeking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seeking_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeavestatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_status', models.BooleanField(default=False)),
                ('leave_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveauthorityPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leaveauthority_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpanel.AllPost')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveseekingPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leaveforwarding_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forwarding', to='userpanel.AllPost')),
                ('leavesanctioning_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sanctioning', to='userpanel.AllPost')),
                ('leaveseeking_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpanel.AllPost')),
            ],
        ),
        migrations.CreateModel(
            name='ReplacingEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replacing_academic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academic', to=settings.AUTH_USER_MODEL)),
                ('replacing_administrative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administrative', to=settings.AUTH_USER_MODEL)),
                ('replacing_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='employeeleaveseeking',
            name='seeking_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpanel.LeaveseekingPost'),
        ),
        migrations.AddField(
            model_name='employeeleaveauthority',
            name='authority_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpanel.LeaveauthorityPost'),
        ),
    ]