#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper, idmquery
from datetime import datetime, timedelta
from libs.logger import errlog_org, infolog_org, debuglog_sys
import xml.etree.ElementTree as Et
from libs.func import incdate


def area_org_inc():
    CURRENT_DATE = datetime.today()
    timestr = datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    idmid = 'AD_SUNAC_301_' + timestr
    WSDL_URL = "http://esb.sunac.com.cn:8002/WP_SUNAC/APP_PUBLIC_SERVICES" \
               "/Proxy_Services/TA_IDM/PUBLIC_SUNAC_301_queryIdmOrgData_PS?wsdl"
    # WSDL_URL = "http://esbqas.sunac.com.cn:8001/WP_SUNAC/APP_PUBLIC_SERVICES" \
    #                 "/Proxy_Services/TA_IDM/PUBLIC_SUNAC_301_queryIdmOrgData_PS?wsdl"
    # SYSTEMID = 'Sunac_IDMOrg'
    SYSTEMID = 'Sunac_AD_ORG'

    dbconn = MysqlOper()
    # IDM一天的增量查询，确定开始和结束时间。
    inc_begindate = dbconn.dbonequery('select inc_datetime from idm_inc_flag where inc_type="org" ')
    begintime = datetime.strftime(inc_begindate[0], '%Y-%m-%d %H:%M:%S.%f')
    inc_enddate = inc_begindate[0] + timedelta(days=2)
    endtime = datetime.strftime(inc_enddate, '%Y-%m-%d %H:%M:%S.%f')
    # 查询IDM增量数据
    try:
        NUM = 1
        NUM_LOOP = 'YES'
        # 查询增量 循环支持的最大页，每页100条数据，如果查询到的当前页小于100条 停止页面循环，如果等于100条，查询下一页
        while NUM <= 999 and NUM_LOOP == 'YES':
            residmorg = idmquery(WSDL_URL, begintime, endtime, NUM, SYSTEMID, idmid, 'idmorg')
            print(residmorg)
            if residmorg['body']['HEADER']['RESULT'] == '0':
                org_list = residmorg['body']['LIST']
                # 解析获取的soap信息
                xml_tree = Et.fromstring(org_list)
                # 如果当天有新增数据，停止增加天数
                if len(xml_tree) > 0:
                    l_orginfo = []
                    for orginfo in xml_tree.iter('ORG'):
                        organnumber = orginfo.find('OrganNumber').text
                        organname = orginfo.find('OrganName').text
                        organparentno = orginfo.find('OrganParentNo').text
                        organupdate = orginfo.find('OrganUpdate').text
                        organcreate = orginfo.find('OrganCreate').text
                        organdep = orginfo.find('OrganDisplayName').text

                        if organdep is not None and organdep.startswith('融创中国_集团本部'):
                            areaid = '000101'
                        elif organdep is not None and organdep.startswith('融创中国_华北区域'):
                            areaid = '000102'
                        elif organdep is not None and organdep.startswith('融创中国_北京区域'):
                            areaid = '000104'
                        elif organdep is not None and organdep.startswith('融创中国_西南区域'):
                            areaid = '000107'
                        elif organdep is not None and organdep.startswith('融创中国_上海区域'):
                            areaid = '000120'
                        elif organdep is not None and organdep.startswith('融创中国_东南区域'):
                            areaid = '000121'
                        elif organdep is not None and organdep.startswith('融创中国_华中区域'):
                            areaid = '000122'
                        elif organdep is not None and organdep.startswith('融创中国_华南区域'):
                            areaid = '000123'
                        elif organdep is not None and organdep.startswith('融创中国_服务集团'):
                            areaid = '0004'
                        elif organdep is not None and organdep.startswith('融创中国_文旅集团'):
                            areaid = '0.04'
                        elif organdep is not None and organdep.startswith('融创中国_文化集团'):
                            areaid = '0.01'
                        else:
                            areaid = '000'

                        organstatus = orginfo.find('OrganStatus').text
                        orgobject = (organnumber, organname, organparentno, organupdate, organcreate,
                                     organdep, organstatus, areaid)
                        l_orginfo.append(orgobject)
                    res_insert = dbconn.dbmanyinsert('replace into idm_org_data(organnumber,organname,organparentno,'
                                                     'organupdate,organcreate,organdep,organstatus,areaid) '
                                                     'values (%s,%s,%s,%s,%s,%s,%s,%s)', l_orginfo)
                    # 判断组织插入是否成功，如果成功查询翻页记录
                    if res_insert:
                        infolog_org('IDM信息--查询时间：%s 至 %s，结果集当前分页：%s，变更组织数：%s' %
                                    (begintime, endtime, NUM, len(xml_tree)))
                        if len(xml_tree) == 100:
                            NUM += 1
                        else:
                            infolog_org('IDM信息--没有更多的翻页数据')
                            NUM_LOOP = 'NO'
                            # 判断增量的日期，插入增量标志作为下次增量查询的开始时间
                            incdate(inc_enddate, CURRENT_DATE, 'org')
                    else:
                        errlog_org('IDM信息--组织插入失败')
                else:
                    infolog_org('IDM信息--查询时间：%s 至 %s，没有查询到增量组织' % (begintime, endtime))
                    NUM_LOOP = 'NO'
                    # 判断增量的日期，插入增量标志作为下次增量查询的开始时间
                    incdate(inc_enddate, CURRENT_DATE, 'org')
            else:
                errlog_org('IDM信息--组织查询接口出现错误')
                NUM_LOOP = 'NO'
    except Exception as e:
        errlog_org(e)
    # 关闭数据库连接
    finally:
        dbconn.dbclose()
