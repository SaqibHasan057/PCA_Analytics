# Generated by Django 2.1.1 on 2018-10-30 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterfaceapp', '0003_twitterdataread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterdataread',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
