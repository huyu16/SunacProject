#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper
from libs.logger import infolog_org, errlog_org


def area_org_handle(v_area, levelnum):
    dbconn = MysqlOper()

    orghandlenum = dbconn.dbonequery('select count(0) from idm_org_handle where areaid = %s', v_area)
    if orghandlenum[0] == 0:
        org_basic = dbconn.dbmanyquery('select organnumber,organname,organparentno,organupdate,organcreate,'
                                       'organdep,organstatus,areaid from idm_org_data where areaid = %s', v_area)
    else:
        org_incdate = dbconn.dbonequery('select max(organupdate) from idm_org_handle '
                                        'where areaid = %s', v_area)
        org_basic = dbconn.dbmanyquery('select organnumber,organname,organparentno,organupdate,organcreate,'
                                       'organdep,organstatus,areaid from idm_org_data '
                                       'where organupdate > %s and areaid = %s', org_incdate[0], v_area)
    if len(org_basic) > 0:
        l_orginfo = []
        for objbasicorg in org_basic:
            l_orglongnamestr = []
            organnumber = objbasicorg[0]
            organname = objbasicorg[1]
            organparentno = objbasicorg[2]
            organupdate = objbasicorg[3]
            organcreate = objbasicorg[4]
            organstatus = objbasicorg[6]
            areaid = objbasicorg[7]

            organdisplayname = objbasicorg[5]
            if organdisplayname is not None:
                l_orglongname = organdisplayname.split('_')
                organlevel = len(l_orglongname)
                for index in range(organlevel):
                    if l_orglongname[index] == '融创中国':
                        l_orglongname[index] = '融创集团'
                        l_orglongnamestr.append('OU=' + l_orglongname[index])
                    else:
                        l_orglongnamestr.append('OU=' + l_orglongname[index])
                l_orglongnamestr.reverse()
                organdep = (','.join(l_orglongnamestr) + ',DC=testing,DC=local')
            else:
                organdep = 'no idm organization'
                organlevel = 0

            if organdisplayname is not None and organdisplayname.startswith('融创中国') \
                    and organstatus == 'Active':
                obj_idmorg = dbconn.dbonequery(
                    'select organnumber, organname, organparentno, organdep, organhandled from idm_org_handle '
                    'where organnumber = %s ', organnumber)

                if organdisplayname.startswith('融创中国_融创集团_'):
                    pre_orgparentno = "Special preorg num"
                    pre_orgdep = "Special preorg"
                    organhandled = 4
                elif organlevel > levelnum:
                    pre_orgparentno = "not required pre org num"
                    pre_orgdep = "not required pre org"
                    organhandled = 6
                elif obj_idmorg is None:
                    pre_orgparentno = "no pre Organization Num"
                    pre_orgdep = "no pre Organization"
                    organhandled = 11
                else:
                    pre_orgparentno = obj_idmorg[2]
                    pre_orgdep = obj_idmorg[3]
                    if obj_idmorg[4] == 11:
                        organhandled = 11
                    elif organname != obj_idmorg[1] and organparentno == pre_orgparentno:
                        organhandled = 12
                    elif organname == obj_idmorg[1] and organparentno != pre_orgparentno:
                        organhandled = 13
                    elif organname == obj_idmorg[1] and organparentno == pre_orgparentno \
                            and organdep != pre_orgdep:
                        organhandled = 5
                    else:
                        organhandled = 3
            else:
                organhandled = 0
                pre_orgparentno = "Error pre Organization Num"
                pre_orgdep = "Error pre Organization"
            orgobject = (organnumber, organname, organparentno, organupdate, organcreate,
                         organdep, organlevel, organstatus, pre_orgparentno, pre_orgdep, organhandled, areaid)
            l_orginfo.append(orgobject)
        res_insert = dbconn.dbmanyinsert('replace into idm_org_handle(organnumber,organname,organparentno,organupdate,'
                                         'organcreate,organdep,organlevel,organstatus,pre_orgparentno,pre_orgdep,'
                                         'organhandled,areaid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', l_orginfo)
        if res_insert:
            infolog_org('IDM信息--区域编号"%s" 已处理组织原始数据信息：%s条' % (v_area, len(org_basic)))
    else:
        infolog_org('IDM信息--区域编号"%s" 没有新的组织需要做处理' % v_area)

    dbconn.dbclose()
