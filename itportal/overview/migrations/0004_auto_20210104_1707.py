# Generated by Django 3.1.1 on 2021-01-04 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0003_auto_20201029_1905'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='host_notmonitor',
            new_name='HostNotmonitor',
        ),
    ]