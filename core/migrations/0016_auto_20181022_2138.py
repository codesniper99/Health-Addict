# Generated by Django 2.0.3 on 2018-10-22 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20181022_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rejected_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rejected_name', models.ManyToManyField(blank=True, related_name='rejected_name', to='core.Names')),
            ],
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='rejected_list',
        ),
        migrations.AddField(
            model_name='mentor',
            name='rejected_list',
            field=models.ManyToManyField(blank=True, related_name='rejected_list', to='core.Rejected_list'),
        ),
    ]
