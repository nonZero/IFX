# Generated by Django 2.0.2 on 2018-04-20 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editing_logs', '0004_logitemrow_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logitem',
            options={'verbose_name': 'log item', 'verbose_name_plural': 'log items'},
        ),
        migrations.AlterModelOptions(
            name='logitemrow',
            options={'verbose_name': 'log item row', 'verbose_name_plural': 'log item rows'},
        ),
    ]
