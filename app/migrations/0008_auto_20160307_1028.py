# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-07 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160304_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='zipcode',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
    ]