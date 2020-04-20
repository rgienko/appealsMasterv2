# Generated by Django 2.1.15 on 2020-04-20 21:03

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200420_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal_master',
            name='case_number',
            field=models.CharField(max_length=7, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='issue_master',
            name='long_description',
            field=tinymce.models.HTMLField(blank=True, max_length=4000, null=True),
        ),
    ]
