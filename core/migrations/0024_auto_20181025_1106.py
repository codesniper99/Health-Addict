# Generated by Django 2.0.3 on 2018-10-25 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20181024_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saccepted_list',
            name='saccepted_name',
        ),
        migrations.AddField(
            model_name='saccepted_list',
            name='saccepted_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
