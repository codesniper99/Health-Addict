# Generated by Django 2.0.3 on 2018-10-20 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20181020_2002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentor',
            old_name='refral_count',
            new_name='referral_count',
        ),
        migrations.RenameField(
            model_name='trainee',
            old_name='refral_count',
            new_name='referral_count',
        ),
    ]
