# Generated by Django 2.0.3 on 2018-10-24 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_referral_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accepted_list',
            name='accepted_name',
        ),
        migrations.RemoveField(
            model_name='pending_list',
            name='pending_name',
        ),
        migrations.RemoveField(
            model_name='rejected_list',
            name='rejected_name',
        ),
        migrations.RemoveField(
            model_name='submentor',
            name='accepted_list',
        ),
        migrations.RemoveField(
            model_name='submentor',
            name='pending_list',
        ),
        migrations.RemoveField(
            model_name='submentor',
            name='rejected_list',
        ),
        migrations.AlterField(
            model_name='mentor',
            name='accepted_list',
            field=models.ManyToManyField(blank=True, related_name='accepted_list', to='core.SubMentor'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='pending_list',
            field=models.ManyToManyField(blank=True, related_name='pending_list', to='core.SubMentor'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='rejected_list',
            field=models.ManyToManyField(blank=True, related_name='rejected_list', to='core.SubMentor'),
        ),
        migrations.DeleteModel(
            name='Accepted_list',
        ),
        migrations.DeleteModel(
            name='Names',
        ),
        migrations.DeleteModel(
            name='Pending_list',
        ),
        migrations.DeleteModel(
            name='Rejected_list',
        ),
    ]