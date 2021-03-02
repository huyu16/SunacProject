#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import ris
from data import zabbix
from django.db.models import Max
from overview.models import host_notmonitor, UserExpire, RisTempUser
from django.core.mail import send_mail
from datetime import datetime, timedelta


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


def monitor_expireuser():
    res_tempuser = UserExpire.objects.filter(expiretime__isnull=False). \
        values('id', 'username', 'company', 'phone', 'email', 'state', 'expiretime', 'manager')
    return res_tempuser


def insert_ristempuser():
    l_risuser = []
    auth_token = ris.gettoken()
    userinf = ris.get_extuser(auth_token)
    ris.getoff(auth_token)

    for obj_userinf in userinf['content']:
        s_risuser = RisTempUser(userid=obj_userinf['loginName'])
        l_risuser.append(s_risuser)
    RisTempUser.objects.all().delete()
    RisTempUser.objects.bulk_create(l_risuser)


def warnning_expireuser():
    cur_datetime = datetime.today()
    sevenday = datetime.strftime(cur_datetime - timedelta(days=-7), '%Y-%m-%d')
    fifteenday = datetime.strftime(cur_datetime - timedelta(days=-15), '%Y-%m-%d')
    # 查询过期时间还有15天和7天的用户
    res_alertuser = UserExpire.objects.filter(expiretime__in=(sevenday, fifteenday), state='active'). \
        values('userid', 'username', 'company', 'phone', 'email', 'expiretime', 'manager')
    if res_alertuser.count() > 0:
        # 查询堡垒机现有临时用户
        l_risuser = []
        q_risuser = RisTempUser.objects.all().values('userid')
        for obj_risuser in q_risuser:
            l_risuser.append(obj_risuser['userid'])

        for obj_alertuser in res_alertuser:
            if obj_alertuser['company']:
                alertuser_company = obj_alertuser['company']
            else:
                alertuser_company = '未登记'
            if obj_alertuser['phone']:
                alertuser_phone = obj_alertuser['phone']
            else:
                alertuser_phone = '未登记'
            if obj_alertuser['email']:
                alertuser_email = obj_alertuser['email']
            else:
                alertuser_email = '未登记'
            send_subject = '您管理的临时用户账号即将过期，请处理！'
            send_body = '过期时间：' + str(obj_alertuser['expiretime']) + '\n用户账号：' + \
                        obj_alertuser['userid'] + \
                        '\n用户姓名：' + obj_alertuser['username'] + '\n用户公司：' + alertuser_company + \
                        '\n用户电话：' + alertuser_phone + '\n用户邮件：' + alertuser_email
            # 如果过期的用户id属于堡垒机用户，给账号管理员和堡垒机管理员发送邮件
            if obj_alertuser['userid'].lower() in l_risuser:
                if obj_alertuser['manager'] is None or obj_alertuser['manager'] == '':
                    recive_user = ['huy33@sunac.com.cn']
                else:
                    recive_user = ['huy33@sunac.com.cn', obj_alertuser['manager']]
                send_mail(send_subject, send_body, 'report@sunac.com.cn', recive_user)
            # 如果过期用户id不属于堡垒机用户，仅给账号管理员发送邮件
            else:
                if obj_alertuser['manager'] is None or obj_alertuser['manager'] == '':
                    pass
                else:
                    send_mail(send_subject, send_body, 'report@sunac.com.cn', obj_alertuser['manager'])
