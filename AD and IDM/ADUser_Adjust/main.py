#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.adorg.idm_org_inc import area_org_inc
from app.adorg.idm_org_handle import area_org_handle
from app.adorg.ad_org_exec import area_org_exec
from app.aduser.idm_user_inc import area_user_inc
from app.aduser.idm_user_handle import area_user_handle
from app.aduser.ad_user_exec import area_user_exec
from libs.connect import MysqlOper
from app.adcomp.ad_comp_exec import area_comp_exec

dbconn = MysqlOper()
areainfo = dbconn.dbmanyquery('select areaname, areaid, adorglevel '
                              'from sum_inf_area where parentid = 0 '
                              'and compprefix in ("BJ","JT","HZ","HB","HN","XN","DN")')

try:
    if __name__ == '__main__':
        # 执行IDM组织数据增量同步
        area_org_inc()
        # 执行IDM用户数据增量同步
        area_user_inc()

        for objarea in areainfo:
            # 执行区域组织数据过滤处理
            area_org_handle(objarea[0], objarea[1], objarea[2])
            # 区域组织数据根据定制规则进行处理
            area_org_exec(objarea[0], objarea[1])
            # 执行区域用户组织数据过滤处理
            area_user_handle(objarea[0], objarea[1], objarea[2])
            # 区域用户数据根据定制规则进行处理
            area_user_exec(objarea[0], objarea[1])
            # 处理区域计算机账号
            area_comp_exec(objarea[0], objarea[1])
except Exception as e:
    print(e)
