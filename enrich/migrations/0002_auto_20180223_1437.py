# Generated by Django 2.0.2 on 2018-02-23 12:37

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query_utils


class Migration(migrations.Migration):

    dependencies = [
        ('enrich', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=django.db.models.query_utils.Q(model__in=('person', 'movie')), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='entity type'),
        ),
    ]