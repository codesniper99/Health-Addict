# Generated by Django 2.0.3 on 2018-10-24 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_names_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SAccepted_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SPending_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SRejected_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='accepted_list',
            name='saccepted_name',
        ),
        migrations.RemoveField(
            model_name='pending_list',
            name='spending_name',
        ),
        migrations.RemoveField(
            model_name='rejected_list',
            name='srejected_name',
        ),
        migrations.AlterField(
            model_name='names',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='submentor',
            name='saccepted_list',
            field=models.ManyToManyField(blank=True, related_name='saccepted_list', to='core.SAccepted_list'),
        ),
        migrations.AlterField(
            model_name='submentor',
            name='spending_list',
            field=models.ManyToManyField(blank=True, related_name='spending_list', to='core.SPending_list'),
        ),
        migrations.AlterField(
            model_name='submentor',
            name='srejected_list',
            field=models.ManyToManyField(blank=True, related_name='srejected_list', to='core.SRejected_list'),
        ),
        migrations.AddField(
            model_name='srejected_list',
            name='srejected_name',
            field=models.ManyToManyField(blank=True, related_name='srejected_name', to='core.Names'),
        ),
        migrations.AddField(
            model_name='spending_list',
            name='spending_name',
            field=models.ManyToManyField(blank=True, related_name='spending_name', to='core.Names'),
        ),
        migrations.AddField(
            model_name='saccepted_list',
            name='saccepted_name',
            field=models.ManyToManyField(blank=True, related_name='saccepted_name', to='core.Names'),
        ),
    ]