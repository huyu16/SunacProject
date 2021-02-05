#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import ris
from data import zabbix
import os
import django
from django.db.models import Max
from overview.models import host_notmonitor
import pymysql

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itportal.settings")
django.setup()


def ris_data():
    auth_token = ris.gettoken()
    devinfset = ris.get_devinf(auth_token)
    dev_list = []
    ris_data_totle = {'total': devinfset['totalElements'], 'rows': dev_list}
    for devinf in devinfset['content']:
        dev_list.append({
            'id': devinf['id'],
            'name': devinf['name'],
            'ip': devinf['ip'],
            'owner_login': devinf['owner']['loginName'],
            'owner_name': devinf['owner']['userName'],
            'department': devinf['department']['name'],
            'state': devinf['state'],
            'deleted': devinf['deleted'],
            'joinTime': devinf['joinTime'],
            'updateTime': devinf['updateTime']
        })
    return ris_data_totle


def zabbix_data():
    zhostsset = zabbix.get_zhosts()
    zhostlist = []
    for zhostinf in zhostsset:
        for zhost_interface in zhostinf['interfaces']:
            if zhost_interface.get('main') == '1':
                zhostlist.append(zhost_interface['ip'])
    return zhostlist


def ris_noesxi():
    ris_hosts = ris_data()['rows']
    for ris_host in ris_hosts[:]:
        if ris_host['name'].find('ESXI主机') != -1:
            ris_hosts.remove(ris_host)
    return ris_hosts


def monitor_data():
    data_list = []
    for ris_host_inf in ris_noesxi():
        if ris_host_inf['ip'] not in zabbix_data():
            data_list.append(ris_host_inf)
    return data_list


def insert_data():
    set_data = monitor_data()
    list_risdata = []
    # 获取ris的updatetime最大值
    for object_risdata in set_data:
        list_risdata.append(object_risdata['updateTime'])
    object_max_ristime = max(list_risdata)
    # 获取数据库的updatetime最大值
    object_max_dbtime = host_notmonitor.objects.aggregate(Max('updateTime'))
    # object_count = host_notmonitor.objects.count()
    # 插入数据库数据
    # if object_count == 0:
    if object_max_ristime > object_max_dbtime['updateTime__max']:
        host_notmonitor.objects.all().delete()

        host_moinitor_list = []
        for host_data in set_data:
            host_object = host_notmonitor(id=host_data['id'], name=host_data['name'],
                                          ip=host_data['ip'],
                                          owner=host_data['owner_login'] + '(' + host_data['owner_name'] + ')',
                                          department=host_data['department'],
                                          state=host_data['state'], deleted=host_data['deleted'],
                                          joinTime=host_data['joinTime'], updateTime=host_data['updateTime'])
            host_moinitor_list.append(host_object)
        host_notmonitor.objects.bulk_create(host_moinitor_list)
    else:
        pass

