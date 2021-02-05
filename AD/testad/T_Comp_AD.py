#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from testad.t_logger import infolog_comp, errlog_comp
from ldap3 import Server, Connection
from testad.t_computer import comparea

server = Server('192.168.4.100')
adconn = Connection(server, 'testing\\admin_adsrv', 'Sunac2020', auto_bind=True)

try:
    # 绑定Mysql数据库
    dbconn = pymysql.connect(
        host='10.4.64.2',
        user='aduser',
        passwd='ADuser@123',
        db='test_ad',
        charset='utf8')
    dbcursor = dbconn.cursor()

    dbcursor.execute('select areacode,areadn from sum_inf_area order by parentid')
    t_areadn = dbcursor.fetchall()

    for obj_areadn in t_areadn:
        querycompou = adconn.search(search_base='OU=融创集团,DC=testing,DC=local',
                                    search_filter=f'(ou={obj_areadn[0]})'
                                    )
        if querycompou:
            pass
        else:
            adconn.add(obj_areadn[1], 'organizationalUnit')
            infolog_comp(f'AD信息--区域计算机OU已创建，{obj_areadn[1]}')
    # 执行北京区域计算机帐号自动调整
    comparea('000104')
    # 执行西南区域计算机帐号自动调整
    comparea('000107')

except Exception as e:
    errlog_comp(e)

finally:
    adconn.unbind()
    dbcursor.close()
    dbconn.close()
