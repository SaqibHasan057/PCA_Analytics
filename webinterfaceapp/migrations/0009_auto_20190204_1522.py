# Generated by Django 2.1.1 on 2019-02-04 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webinterfaceapp', '0008_auto_20190204_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockdata',
            old_name='dimention',
            new_name='dimension',
        ),
    ]
