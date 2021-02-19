#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import AdOper, MysqlOper
from libs.logger import infolog_comp, errlog_comp
from libs.func import for_compmove


def area_comp_exec(v_areaname, v_area):
    adconn = AdOper()
    dbconn = MysqlOper()

    t_areainfo = dbconn.dbmanyquery('select areadn from sum_inf_area '
                                    'where status = 1 and parentid =%s order by parentid', v_area)
    # 创建区域定义的计算机OU
    for obj_area in t_areainfo:
        adfilter = '(distinguishedName=' + obj_area[0] + ')'
        querycompou = adconn.adquery('OU=融创集团,DC=SUNAC,DC=local', adfilter)
        if querycompou:
            pass
        else:
            resadou = adconn.adadd(obj_area[0], 'organizationalUnit')
            if resadou:
                infolog_comp(f'AD信息--区域计算机OU创建成功，{obj_area[0]}')

    # 查询computers OU下的以当前区域代码为前缀的计算机
    adcompprefix = dbconn.dbonequery('select compprefix, areaname from sum_inf_area where areaid = %s', v_area)
    adconn.adattrquery('CN=Computers,DC=SUNAC,DC=local', f"(&(objectClass=computer)(name={adcompprefix[0]}*))", 'name')
    t_adcomp = dbconn.dbmanyquery('select compprefix, areadn, areacode, areaname from sum_inf_area '
                                  'where parentid = %s and status = 1 order by compprefix desc', v_area)
    resadconn = adconn.adconn.response
    if len(resadconn) > 0:
        # 循环当前区域的主机，归类到对应的OU下
        for_compmove(v_areaname, resadconn, t_adcomp)
    else:
        pass

    # 将单个区域下computer OU下的计算机账号归类
    adconn.adattrquery(f"OU=computers,OU={adcompprefix[1]},OU=融创集团,DC=SUNAC,DC=local",
                       f"(&(objectClass=computer)(name={adcompprefix[0]}*))",
                       'name')
    t_adcomp1 = dbconn.dbmanyquery('select compprefix, areadn, areacode, areaname from sum_inf_area '
                                   'where parentid = %s and status = 1 order by compprefix desc', v_area)
    resadconn1 = adconn.adconn.response
    if len(resadconn1) > 0:
        for_compmove(v_areaname, resadconn1, t_adcomp1)
    else:
        pass

    # 查询单个区域下的计算机OU组是否有变更计算机账号，并做相应归类
    t_areaou = dbconn.dbmanyquery('select areacode,compprefix from sum_inf_area where parentid = %s and status = 1',
                                  v_area)
    p_areaou = dbconn.dbonequery('select areacode from sum_inf_area where areaid = %s', v_area)
    t_adcomp2 = dbconn.dbmanyquery('select compprefix, areadn, areacode, areaname from sum_inf_area '
                                   'where status = 1 and parentid<>0 order by compprefix desc')
    for areaou in t_areaou:
        adconn.adattrquery(f"OU={areaou[0]},OU={p_areaou[0]},OU=融创集团,DC=SUNAC,DC=local",
                           f"(&(objectClass=computer)(!(name={areaou[1]}*)))",
                           'name')
        resadconn2 = adconn.adconn.response
        if len(resadconn2) > 0:
            for_compmove(v_areaname, resadconn2, t_adcomp2)
        else:
            pass

    adconn.adclose()
    dbconn.dbclose()
