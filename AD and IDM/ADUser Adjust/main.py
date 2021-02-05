#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.adorg.idm_org_inc import area_org_inc
from app.adorg.idm_org_handle import area_org_handle
from app.adorg.ad_org_exec import area_org_exec

areaid = [('北京区域集团', '000104', 4), ('华南区域集团', '000123', 5)]

if __name__ == '__main__':
    # 执行IDM组织数据增量查询
    # area_org_inc()
    # 执行北京区域组织数据过滤处理
    area_org_handle('000104', 4)
    # 执行华南区域组织数据过滤处理
    # area_org_handle('000123', 5)
    # 根据过滤的数据处理组织
    area_org_exec('000104')

