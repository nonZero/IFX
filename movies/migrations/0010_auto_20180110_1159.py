# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_auto_20180110_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='summary_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='summary_he',
            field=models.TextField(blank=True, null=True),
        ),
    ]
