# Generated by Django 2.1.1 on 2019-02-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterfaceapp', '0006_auto_20190204_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(max_length=5000)),
                ('dimention', models.TextField(max_length=500)),
            ],
        ),
    ]
