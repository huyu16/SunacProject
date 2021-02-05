#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from libs.connect import MysqlOper
from libs.func import incdate

CURRENT_DATE = datetime.datetime.today()
v_area = 'OU=北京区域集团,OU=融创集团,DC=SUNAC,DC=local'

dbconn = MysqlOper()
# maxorgdate = dbconn.dbonequery('select max(organupdate) from dic_idm_org')
# maxusrdate = dbconn.dbonequery('select max(userupdate) from dic_idm_user')
try:
    org_basic = dbconn.dbmanyquery('select organnumber,organname,organparentno,organupdate,organcreate,'
                                   'organdep,organstatus from idm_org_data where organdep like %s', ('%' + v_area))
    print(org_basic)
except Exception as e:
    print(e)

t = dbconn.dbmanyquery('select * from idm_org_data where organdep like "融创中国_北京区域%%" ')
print(t)


# SQL = 'select organnumber,organname,organparentno,organupdate,organcreate,organdep,organstatus from idm_org_data where organupdate > %s and organdep like %s' % (org_incdate[])
#
# org_basic = dbconn.dbmanyquery('select organnumber,organname,organparentno,organupdate,organcreate,'
#                                'organdep,organstatus from idm_org_data '
#                                'where organupdate > %s and organdep like %s', org_incdate[0], v_area)

# print(org_basic)

