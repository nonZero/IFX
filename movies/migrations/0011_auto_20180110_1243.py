# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 12:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20180110_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='description',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='movie_title',
            name='movie',
        ),
        migrations.DeleteModel(
            name='Description',
        ),
        migrations.DeleteModel(
            name='Movie_Title',
        ),
    ]
