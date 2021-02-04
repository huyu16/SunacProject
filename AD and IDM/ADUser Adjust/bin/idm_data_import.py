#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper, excelidm

EXCELORGFILE = \
    r"C:\Users\zxcvb\Documents\CloudStation\My Python\SunacProject\AD and IDM\ADUser Adjust\files\tmp001-org0106.xlsx"
EXCELUSRFILE = \
    r"C:\Users\zxcvb\Documents\CloudStation\My Python\SunacProject\AD and IDM\ADUser Adjust\files\tmp001-usr0106.xlsx"
# 插入IDM组织原始数据到数据库
dbconn = MysqlOper()
# 判断【idm_org_init】是否为空
resorgunm = dbconn.dbonequery('select count(0) from idm_org_data')
if resorgunm[0] == 0:
    orgvalue = excelidm(EXCELORGFILE)
    orgsql = 'insert into idm_org_data(organnumber,organname,organparentno,organupdate,' \
             'organcreate,organdep,organstatus) values (%s,%s,%s,%s,%s,%s,%s)'
    orgres_insert = dbconn.dbmanyinsert(orgsql, orgvalue)
    # 指定组织增量查询的起始时间
    if orgres_insert:
        maxorgdate = dbconn.dbonequery('select max(organupdate) from idm_org_data')
        dbconn.dbonemod('replace into idm_inc_flag values ("org", %s)', maxorgdate[0])
        # 为IDM组织添加区域ID
        dbconn.dbonemod('UPDATE idm_org_data SET areaid = CASE '
                        'WHEN organdep like "融创中国_集团本部%%" THEN "000101" '
                        'WHEN organdep like "融创中国_华北区域%%" THEN "000102" '
                        'WHEN organdep like "融创中国_北京区域%%" THEN "000104" '
                        'WHEN organdep like "融创中国_西南区域%%" THEN "000107" '
                        'WHEN organdep like "融创中国_上海区域%%" THEN "000120" '
                        'WHEN organdep like "融创中国_东南区域%%" THEN "000121" '
                        'WHEN organdep like "融创中国_华中区域%%" THEN "000122" '
                        'WHEN organdep like "融创中国_华南区域%%" THEN "000123" '
                        'WHEN organdep like "融创中国_服务集团%%" THEN "0004" '
                        'WHEN organdep like "融创中国_文旅集团%%" THEN "0.04" '
                        'WHEN organdep like "融创中国_文化集团%%" THEN "0.01" '
                        'ELSE "000" END ')
# 判断【idm_user_init】是否为空
resusernum = dbconn.dbonequery('select count(0) from idm_user_data')
if resusernum[0] == 0:
    usrvalue = excelidm(EXCELUSRFILE)
    usrsql = 'insert into idm_user_data' \
             '(userid,username,userdeptno,olduserorg,userupdate,usercreate,useremptype,userstatus) ' \
             'values (%s,%s,%s,%s,%s,%s,%s,%s)'
    usrres_insert = dbconn.dbmanyinsert(usrsql, usrvalue)
    # 指定用户增量查询的起始时间
    if usrres_insert:
        maxusrdate = dbconn.dbonequery('select max(userupdate) from idm_user_data')
        dbconn.dbonemod('replace into idm_inc_flag values ("user", %s)', maxusrdate[0])
        # 为IDM用户添加区域ID
        dbconn.dbonemod('update idm_user_data t1 left join idm_org_data t2 '
                        'on t1.userdeptno = t2.organnumber '
                        'set t1.userorg = t2.organdep,t1.userareaid = t2.areaid')

dbconn.dbclose()
