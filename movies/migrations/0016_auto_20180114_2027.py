# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-14 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_tag_lang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='type_1',
        ),
        migrations.AddField(
            model_name='tag',
            name='type_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
