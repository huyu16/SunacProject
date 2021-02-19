#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper
from libs.logger import errlog_org, infolog_comp, errlog_comp
from libs.connect import AdOper


def incdate(incdate, curdate, inctype):
    try:
        dbconn = MysqlOper()
        if incdate < curdate:
            inc_flag = incdate
        else:
            inc_flag = curdate
        dbconn.dbonemod('update idm_inc_flag set inc_datetime=%s where inc_type=%s', inc_flag, inctype)
    except Exception as e:
        errlog_org(e)
    finally:
        dbconn.dbclose()


def for_compmove(v_areaname, v_respadconn, v_adcompou):
    v_adconn = AdOper()
    for obj_adcomp in v_respadconn:
        hostname = obj_adcomp['attributes']['name']
        str_hostolddn = obj_adcomp['dn']
        hostolddn = str_hostolddn.split(',')
        hostcn = hostolddn[0]
        l_hostoldou = hostolddn[1:]
        hostoldou = ','.join(l_hostoldou)

        for adcomp in v_adcompou:
            if hostname.startswith(adcomp[0]):
                if hostoldou != adcomp[1]:
                    res_compou = v_adconn.admove(str_hostolddn, hostcn, adcomp[1])
                    if res_compou:
                        infolog_comp(f"AD信息--{v_areaname}，移动计算机帐号成功 {hostname}")
                    else:
                        errlog_comp(f"AD信息--{v_areaname}，移动计算机帐号失败 {hostname}")
                    break
                else:
                    break
    v_adconn.adclose()
