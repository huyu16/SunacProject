#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from testad.t_logger import infolog_org, errlog_org
from ldap3 import Server, Connection

try:
    # 绑定Mysql数据库
    dbconn = pymysql.connect(
        host='10.4.64.2',
        user='aduser',
        passwd='ADuser@123',
        db='test_ad',
        charset='utf8')
    dbcursor = dbconn.cursor()

    server = Server('192.168.4.100')
    adconn = Connection(server, 'testing\\admin_adsrv', 'Sunac2020', auto_bind=True)

    dbcursor.execute('select max(orglevel) from dic_idm_org where orghandled > 9 '
                     'and orgdep like "%OU=上海区域集团,OU=融创集团,DC=testing,DC=local" ')
    maxorglevel = dbcursor.fetchone()[0]
    dbcursor.execute('select min(orglevel) from dic_idm_org where orghandled > 9 '
                     'and orgdep like "%OU=上海区域集团,OU=融创集团,DC=testing,DC=local" ')
    minorglevel = dbcursor.fetchone()[0]

    if maxorglevel is not None:
        while minorglevel <= maxorglevel:
            dbcursor.execute('select organnumber, organname, organparentno, orgdep, pre_orgdep, orghandled '
                             'from dic_idm_org where orglevel = %s and orghandled > 9 '
                             'and orgdep like "%%OU=上海区域集团,OU=融创集团,DC=testing,DC=local"' % minorglevel)
            t_resorg = dbcursor.fetchall()
            if len(t_resorg) > 0:
                for orgobject in t_resorg:
                    if orgobject[-1] in [10, 11]:
                        res_ouadd = adconn.add(orgobject[3], 'organizationalUnit')
                        if res_ouadd:
                            dbcursor.execute('update dic_idm_org set orghandled = 1 where organnumber = "%s" ' %
                                             (orgobject[0]))
                            infolog_org('AD信息--创建成功的OU：%s' % (orgobject[3]))
                        else:
                            errlog_org('AD信息--创建失败的OU：%s' % (orgobject[3]))
                            errlog_org(adconn.result)
                            if adconn.result['result'] == 68:
                                dbcursor.execute('update dic_idm_org set orghandled = 2 where organnumber = "%s" ' %
                                                 (orgobject[0]))
                            else:
                                dbcursor.execute('update dic_idm_org set orghandled = 10 where organnumber = "%s" ' %
                                                 (orgobject[0]))
                    elif orgobject[-1] == 12:
                        res_ourename = adconn.modify_dn(orgobject[4], 'OU=' + orgobject[1])
                        print(res_ourename)
                        if res_ourename:
                            dbcursor.execute('update dic_idm_org set orghandled = 1 where organnumber = "%s" ' %
                                             (orgobject[0]))
                            infolog_org('AD信息--重命名成功的OU：%s' % (orgobject[3]))
                        else:
                            errlog_org('AD信息--重命名失败的OU：%s' % (orgobject[3]))
                            errlog_org(adconn.result)
                            dbcursor.execute('update dic_idm_org set orghandled = 10 where organnumber = "%s" ' %
                                             (orgobject[0]))
                    elif orgobject[-1] == 13:
                        dbcursor.execute('select orgdep from dic_idm_org '
                                         'where organnumber = "%s" ' % (orgobject[2]))
                        orgparent = dbcursor.fetchone()[0]
                        res_oumove = adconn.modify_dn(orgobject[4],
                                                      'OU='+orgobject[1], new_superior=orgparent)
                        if res_oumove:
                            dbcursor.execute('update dic_idm_org set orghandled = 1 where organnumber = "%s" ' %
                                             (orgobject[0]))
                            infolog_org('AD信息--移动成功的OU：%s' % (orgobject[3]))
                        else:
                            errlog_org('AD信息--移动失败的OU：%s' % orgparent)
                            errlog_org(adconn.result)
                            dbcursor.execute('update dic_idm_org set orghandled = 10 where organnumber = "%s" ' %
                                             (orgobject[0]))
                    else:
                        infolog_org('AD信息--无预定义动作')
                        dbcursor.execute('update dic_idm_org set orghandled = 3 where organnumber = "%s" ' %
                                         (orgobject[0]))
            else:
                pass
            minorglevel += 1
            dbconn.commit()
    else:
        infolog_org("AD信息--没有需要处理的OU")

except Exception as e:
    errlog_org(e)

finally:
    adconn.unbind()
    dbcursor.close()
    dbconn.close()
