#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper, excelidm

EXCELORGFILE = r"C:\Users\zxcvb\Documents\CloudStation\My Python\SunacProject\ADUser Adjust\file\tmp001-org0106.xlsx"
EXCELUSRFILE = r"C:\Users\zxcvb\Documents\CloudStation\My Python\SunacProject\ADUser Adjust\file\tmp001-usr0106.xlsx"

# 插入IDM组织原始数据到数据库
orgdbconn = MysqlOper()
# 判断【idm_org_init】是否为空
resorgunm = orgdbconn.dbonequery('select count(0) from idm_org_data')
if resorgunm[0] == 0:
    orgvalue = excelidm(EXCELORGFILE)
    orgsql = 'insert into idm_org_data(organnumber,organname,organparentno,organupdate,' \
             'organcreate,organdep,organstatus) values (%s,%s,%s,%s,%s,%s,%s)'
    orgres_insert = orgdbconn.dbmanyinsert(orgsql, orgvalue)
    # 指定组织增量查询的起始时间
    if orgres_insert:
        maxorgdate = orgdbconn.dbonequery('select max(organupdate) from idm_org_data')
        orgdbconn.dbonemod('replace into idm_inc_flag values ("org", %s)', maxorgdate[0])
orgdbconn.dbclose()

# 插入IDM人员原始数据到数据库
usrdbconn = MysqlOper()
# 判断【idm_user_init】是否为空
resusernum = usrdbconn.dbonequery('select count(0) from idm_user_data')
if resusernum[0] == 0:
    usrvalue = excelidm(EXCELUSRFILE)
    usrsql = 'insert into idm_user_data(userid,username,userdeptno,userorg,userupdate,usercreate,' \
             'useremptype,userstatus) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    usrres_insert = usrdbconn.dbmanyinsert(usrsql, usrvalue)
    # 指定用户增量查询的起始时间
    if usrres_insert:
        maxusrdate = usrdbconn.dbonequery('select max(userupdate) from idm_user_data')
        usrdbconn.dbonemod('replace into idm_inc_flag values ("user", %s)', maxusrdate[0])
usrdbconn.dbclose()

dbconn = MysqlOper()
dbconn.dbonemod('update idm_org_data set areaid = "000101" where organdep like "融创中国_集团本部%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "000102" where organdep like "融创中国_华北区域%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "000104" where organdep like "融创中国_北京区域%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "000107" where organdep like "融创中国_西南区域%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "000120" where organdep like "融创中国_上海区域%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "000121" where organdep like "融创中国_东南区域%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "000122" where organdep like "融创中国_华中区域%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "000123" where organdep like "融创中国_华南区域%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "0004" where organdep like "融创中国_服务集团%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "0.04" where organdep like "融创中国_文旅集团%%" ')
dbconn.dbonemod('update idm_org_data set areaid = "0.01" where organdep like "融创中国_文化集团%%" ')
dbconn.dbclose()
