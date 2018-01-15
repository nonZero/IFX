# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20180108_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_he', models.CharField(max_length=300)),
                ('name_en', models.CharField(max_length=300)),
                ('first_name_he', models.CharField(max_length=300)),
                ('first_name_en', models.CharField(max_length=300)),
                ('last_name_he', models.CharField(max_length=300)),
                ('last_name_en', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='summary_en',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='summary_he',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='title_en',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='title_he',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='description',
            name='lang',
            field=models.CharField(choices=[('he', 'Hebrew'), ('en', 'English')], max_length=300),
        ),
        migrations.AlterField(
            model_name='description',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='description', to='movies.Movie'),
        ),
    ]
