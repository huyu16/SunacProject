# Generated by Django 3.1.1 on 2021-01-04 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0004_auto_20210104_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='host_notmonitor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('ip', models.GenericIPAddressField()),
                ('owner', models.CharField(max_length=30, null=True)),
                ('department', models.CharField(max_length=20)),
                ('state', models.IntegerField()),
                ('deleted', models.BooleanField()),
                ('joinTime', models.BigIntegerField()),
                ('updateTime', models.BigIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='HostNotmonitor',
        ),
    ]
