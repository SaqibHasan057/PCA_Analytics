# Generated by Django 2.1.1 on 2019-02-04 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinterfaceapp', '0005_newsdata_newsdataread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsdataread',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webinterfaceapp.NewsData'),
        ),
    ]
