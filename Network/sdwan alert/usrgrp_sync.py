#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将zabbix用户组的用户信息同步到数据库中，完成zabbix网络告警和sdwan脚本告警人员同步
"""
from pyzabbix import ZabbixAPI
import pymysql

# 创建zabbix连接
zabbixserver = 'http://192.168.7.206/zabbix'
zapi = ZabbixAPI(zabbixserver)
zapi.login("Admin", "Sunac@2018")
# 创建数据库连接，查询用户组
dbconn = pymysql.connect("10.4.64.2", "aduser", "ADuser@123", "ad")
dbcursor = dbconn.cursor()
dbcursor.execute('select areaname,networkmgr from sum_inf_area where parentid = 0')
resuser = dbcursor.fetchall()

for areainfo in resuser:
    str_areauser = areainfo[1]
    l_areauser = str_areauser.split('|')

    set_user = set()
    userlist = zapi.usergroup.get(
        output=['name'],
        selectUsers=['alias', 'name'],
        search={'name': areainfo[0]}
    )
    if len(userlist) > 0:
        for userinfo in userlist[0]['users']:
            set_user.add(userinfo['alias'])
        if len(set_user) > 0 and set_user != set(l_areauser):
            alertuser = '|'.join(set_user)
            dbcursor.execute('update sum_inf_area set networkmgr = %s '
                             'where areaname = %s and parentid = 0', (alertuser, areainfo[0]))
            dbconn.commit()
        else:
            pass

dbcursor.close()
dbconn.close()
