# Generated by Django 2.1.15 on 2020-04-15 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200414_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='critical_dates_master',
            name='critical_date',
            field=models.DateTimeField(),
        ),
    ]
