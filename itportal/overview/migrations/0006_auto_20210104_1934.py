# Generated by Django 3.1.1 on 2021-01-04 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0005_auto_20210104_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexpire',
            name='manager',
            field=models.CharField(default='huy33', max_length=20),
        ),
    ]
