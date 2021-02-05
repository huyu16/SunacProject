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
    userid = models.CharField(max_length=20, primary_key=True)
    username = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    state = models.CharField(max_length=10)
    expiretime = models.DateTimeField()
    manager = models.CharField(max_length=20, default='huy33')
    updatetime = models.DateTimeField()
    createtime = models.DateTimeField()
