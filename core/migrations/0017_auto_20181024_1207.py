# Generated by Django 2.0.3 on 2018-10-24 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20181022_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='submentor',
            name='accepted_list',
            field=models.ManyToManyField(blank=True, related_name='saccepted_list', to='core.Accepted_list'),
        ),
        migrations.AddField(
            model_name='submentor',
            name='pending_list',
            field=models.ManyToManyField(blank=True, related_name='spending_list', to='core.Pending_list'),
        ),
        migrations.AddField(
            model_name='submentor',
            name='rejected_list',
            field=models.ManyToManyField(blank=True, related_name='srejected_list', to='core.Rejected_list'),
        ),
    ]
