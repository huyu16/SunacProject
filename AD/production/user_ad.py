#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from .logger import infolog_user, errlog_user
from ldap3 import Server, Connection, SUBTREE

try:
    # 绑定Mysql数据库
    dbconn = pymysql.connect(
        host='10.4.64.2',
        user='aduser',
        passwd='ADuser@123',
        db='ad',
        charset='utf8')
    dbcursor = dbconn.cursor()

    server = Server('192.168.4.100')
    adconn = Connection(server, 'testing\\admin_adsrv', 'Sunac2020', auto_bind=True)

    dbcursor.execute('select userid,userorg from dic_idm_user where userhandled > 9')
    processed_user = dbcursor.fetchall()
    for userobj in processed_user:

        adquery = adconn.search(search_base='ou=融创集团,dc=testing,dc=local',
                                search_filter=f'(&(objectClass=person)(sAMAccountName={userobj[0].lower()})'
                                              f'(!(userAccountControl=514)))')
        if adquery:
            for aduserobj in adconn.response:
                pre_userorg = aduserobj['dn']
                l_userorg = pre_userorg.split(',')
                userobjcn = l_userorg[0]
                userobjou = ','.join(l_userorg[1:])
                if userobjou != userobj[1]:
                    res_admodify = adconn.modify_dn(pre_userorg, userobjcn, new_superior=userobj[1])
                    if res_admodify:
                        dbcursor.execute('update dic_idm_user set pre_userorg = "%s", '
                                         'userhandled = 1 where userid = "%s" '
                                         % (pre_userorg, userobj[0]))
                        infolog_user('AD信息--已移动到新OU的用户：%s' % (userobj[0]))
                    else:
                        dbcursor.execute('update dic_idm_user set pre_userorg = "%s", '
                                         'userhandled = 10 where userid = "%s" '
                                         % (pre_userorg, userobj[0]))
                        errlog_user('AD信息--移动OU失败的用户：%s' % (userobj[0]))
                        errlog_user(adconn.result)
                else:
                    dbcursor.execute('update dic_idm_user set pre_userorg = "%s", '
                                     'userhandled = 2 where userid = "%s" '
                                     % (pre_userorg, userobj[0]))
                    errlog_user('AD信息--已存在的用户：%s' % (userobj[0]))
        else:
            pre_userorg = 'no ad user'
            dbcursor.execute('update dic_idm_user set pre_userorg = "%s", '
                             'userhandled = 0 where userid = "%s" '
                             % (pre_userorg, userobj[0]))
            errlog_user('AD信息--没有创建的用户：%s' % (userobj[0]))

    dbconn.commit()

except Exception as e:
    errlog_user(e)

finally:
    adconn.unbind()
    dbcursor.close()
    dbconn.close()
