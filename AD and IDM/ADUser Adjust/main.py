#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.adorg.idm_org_inc import area_org_inc
from app.adorg.idm_org_handle import area_org_handle
from app.adorg.ad_org_exec import area_org_exec
from app.aduser.idm_user_inc import area_user_inc
from app.aduser.idm_user_handle import area_user_handle
from app.aduser.ad_user_exec import area_user_exec

areainfo = [('北京区域集团', '000104', 4), ('东南区域集团', '000123', 4)]

if __name__ == '__main__':
    # 执行IDM组织数据增量同步
    area_org_inc()
    # 执行IDM用户数据增量同步
    area_user_inc()

    for v_area in areainfo:
        # 执行区域组织数据过滤处理
        area_org_handle(v_area[1], v_area[2])
        # 区域组织数据根据定制规则进行处理
        area_org_exec(v_area[1])
        # 执行区域用户组织数据过滤处理
        area_user_handle(v_area[1], v_area[2])
        # 区域用户数据根据定制规则进行处理
        area_user_exec(v_area[1])
