#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.logger import infolog_org, errlog_org
from libs.connect import AdOper, MysqlOper


def area_org_exec(v_areaname, v_area):
    # 绑定Mysql数据库
    dbconn = MysqlOper()
    adconn = AdOper()

    t_maxorglevel = dbconn.dbonequery('select max(organlevel) from idm_org_handle where organhandled > 9 '
                                      'and areaid=%s', v_area)
    t_minorglevel = dbconn.dbonequery('select min(organlevel) from idm_org_handle where organhandled > 9 '
                                      'and areaid=%s', v_area)
    maxorglevel = t_maxorglevel[0]
    minorglevel = t_minorglevel[0]
    try:
        if maxorglevel is not None:
            while minorglevel <= maxorglevel:
                t_resorg = dbconn.dbmanyquery(
                    'select organnumber, organname, organparentno, organdep, pre_orgdep, organhandled from idm_org_handle where organlevel = %s and organhandled > 9 and areaid = %s',
                    minorglevel, v_area)
                if len(t_resorg) > 0:
                    for orgobject in t_resorg:
                        adfilter = '(distinguishedName=' + orgobject[3] + ')'
                        res_adquery = adconn.adquery('ou=融创集团,dc=SUNAC,dc=local', adfilter)
                        if res_adquery:
                            dbconn.dbonemod('update idm_org_handle set organhandled = 2 '
                                            'where organnumber = %s ', (orgobject[0]))
                            infolog_org('AD信息--组织已存在：%s' % orgobject[3])
                        else:
                            if orgobject[5] in [10, 11]:
                                res_ouadd = adconn.adadd(orgobject[3], 'organizationalUnit')
                                if res_ouadd:
                                    dbconn.dbonemod('update idm_org_handle set organhandled = 1 '
                                                    'where organnumber = %s ', (orgobject[0]))
                                    infolog_org('AD信息--创建成功的OU：%s' % (orgobject[3]))
                                else:
                                    errlog_org('AD信息--创建失败的OU：%s' % (orgobject[3]))
                                    dbconn.dbonemod('update idm_org_handle set organhandled = 10 '
                                                    'where organnumber = %s ', (orgobject[0]))
                            elif orgobject[5] == 12:
                                res_ourename = adconn.adrename(orgobject[4], 'OU=' + orgobject[1])
                                if res_ourename:
                                    dbconn.dbonemod('update idm_org_handle set organhandled = 1 '
                                                    'where organnumber = %s ', (orgobject[0]))
                                    infolog_org('AD信息--重命名成功的OU：%s' % (orgobject[3]))
                                else:
                                    errlog_org('AD信息--重命名失败的OU：%s' % (orgobject[3]))
                                    dbconn.dbonemod('update idm_org_handle set organhandled = 10 '
                                                    'where organnumber = %s ', (orgobject[0]))
                            elif orgobject[5] == 13:
                                orgparent = dbconn.dbonequery('select organdep from idm_org_handle '
                                                              'where organnumber = %s ', (orgobject[2]))
                                res_oumove = adconn.admove(orgobject[4], 'OU=' + orgobject[1], orgparent[0])
                                if res_oumove:
                                    dbconn.dbonemod('update idm_org_handle set organhandled = 1 '
                                                    'where organnumber = %s ', (orgobject[0]))
                                    infolog_org('AD信息--移动成功的OU：%s' % (orgobject[3]))
                                else:
                                    errlog_org('AD信息--移动失败的OU：%s' % (orgobject[3]))
                                    dbconn.dbonemod('update idm_org_handle set organhandled = 10 '
                                                    'where organnumber = %s ', (orgobject[0]))
                            else:
                                infolog_org('AD信息--无预定义动作')
                                dbconn.dbonemod('update dic_idm_org set orghandled = 3 '
                                                'where organnumber = %s ', (orgobject[0]))
                else:
                    infolog_org('AD信息--区域"%s" 没有需要处理的OU' % v_areaname)
                minorglevel += 1
        else:
            infolog_org('AD信息--区域"%s" 没有新增需要处理的OU' % v_areaname)

    except Exception as e:
        errlog_org(repr(e))

    finally:
        adconn.adclose()
        dbconn.dbclose()
