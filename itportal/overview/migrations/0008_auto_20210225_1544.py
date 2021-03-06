# Generated by Django 3.1.1 on 2021-02-25 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0007_auto_20210224_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='userexpire',
            name='usertype',
            field=models.CharField(default='Temp', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='company',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='createtime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='expiretime',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='manager',
            field=models.CharField(default='huy33', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='state',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userexpire',
            name='updatetime',
            field=models.DateTimeField(null=True),
        ),
    ]
