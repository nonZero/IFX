# Generated by Django 2.0.4 on 2018-04-21 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20180224_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='name_en',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='English name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name_he',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Hebrew name'),
        ),
    ]