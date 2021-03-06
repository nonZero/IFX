# Generated by Django 2.0.2 on 2018-02-23 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielink',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='links', to='movies.Movie'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movielinks', to='links.LinkType'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='links', to='people.Person'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='personlinks', to='links.LinkType'),
        ),
    ]
