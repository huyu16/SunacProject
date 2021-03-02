from django.db import models


# Create your models here.

class host_notmonitor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    owner = models.CharField(max_length=30, null=True)
    department = models.CharField(max_length=20)
    state = models.IntegerField()
    deleted = models.BooleanField()
    joinTime = models.BigIntegerField()
    updateTime = models.BigIntegerField()


class UserExpire(models.Model):
    userid = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20)
    company = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    state = models.CharField(max_length=10, null=True)
    expiretime = models.DateTimeField(null=True)
    manager = models.EmailField(null=True)
    updatetime = models.DateTimeField(null=True)
    createtime = models.DateTimeField(null=True)
    usertype = models.CharField(max_length=20, null=True, default='Temp')

    class Meta:
        indexes = [
            models.Index(fields=['expiretime']),
            ]


class RisTempUser(models.Model):
    userid = models.CharField(max_length=20, primary_key=True)
