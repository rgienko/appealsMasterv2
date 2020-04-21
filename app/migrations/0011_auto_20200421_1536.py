# Generated by Django 2.1.15 on 2020-04-21 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200420_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue_master',
            name='long_description',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='issue_master',
            name='rep_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.srg_staff_master'),
        ),
    ]
