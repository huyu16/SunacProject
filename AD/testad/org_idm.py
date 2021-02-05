#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testad.logger import infolog_org, errlog_org, debuglog_org
import xml.etree.ElementTree as ET
from zeep import Client
from zeep.plugins import HistoryPlugin
from datetime import datetime, timedelta
import pymysql

timestr = datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
idmid = 'AD_SUNAC_301_' + timestr
history = HistoryPlugin()
WSDL_URL = "http://esb.sunac.com.cn:8002/WP_SUNAC/APP_PUBLIC_SERVICES" \
           "/Proxy_Services/TA_IDM/PUBLIC_SUNAC_301_queryIdmOrgData_PS?wsdl"
INITIAL_TIME = datetime.strptime('2020-11-20 00:00:00.000', '%Y-%m-%d %H:%M:%S.%f')
CURRENT_DATE = datetime.today()

try:
    # 绑定Mysql数据库
    dbconn = pymysql.connect(
        host='10.4.64.2',
        user='aduser',
        passwd='ADuser@123',
        db='test_ad',
        charset='utf8')
    dbcursor = dbconn.cursor()

    dbcursor.execute('select count(0) from dic_idm_org')
    rownum = dbcursor.fetchone()[0]

    if rownum == 0:
        begindatetime = INITIAL_TIME + timedelta(seconds=1)
        enddatetime = begindatetime + timedelta(days=1)
        begindatestr = datetime.strftime(begindatetime, '%Y-%m-%d %H:%M:%S.%f')
        enddatestr = datetime.strftime(enddatetime, '%Y-%m-%d %H:%M:%S.%f')
    else:
        dbcursor.execute('SELECT max(organupdate) from dic_idm_org')
        max_organupdate = dbcursor.fetchone()[0]
        begindatetime = max_organupdate + timedelta(seconds=1)
        enddatetime = begindatetime + timedelta(days=1)
        begindatestr = datetime.strftime(begindatetime, '%Y-%m-%d %H:%M:%S.%f')
        enddatestr = datetime.strftime(enddatetime, '%Y-%m-%d %H:%M:%S.%f')

    DATE_LOOP = 'YES'
    while datetime.strptime(begindatestr, '%Y-%m-%d %H:%M:%S.%f') < CURRENT_DATE and DATE_LOOP == 'YES':
        NUM = 1
        NUM_LOOP = 'YES'
        while NUM <= 100 and NUM_LOOP == 'YES':
            client = Client(wsdl=WSDL_URL, plugins=[history])
            querydto_type = client.get_type('ns0:queryDto')
            header_type = client.get_type('ns2:Header')
            querydto = querydto_type(beginDate=begindatestr, endDate=enddatestr,
                                     pageNo=NUM, pageRowNo='100', systemID='Sunac_IDMOrg')
            header = header_type(BIZTRANSACTIONID=idmid, COUNT='', CONSUMER='',
                                 SRVLEVEL='', ACCOUNT='idmadmin', PASSWORD='idmpass')

            r_idmorg = client.service.PUBLIC_SUNAC_301_queryIdmOrgData(queryDto=querydto,
                                                                       _soapheaders={'parameters2': header})
            debuglog_org(history.last_sent)
            debuglog_org(history.last_received)
            if r_idmorg['body']['HEADER']['RESULT'] == '0':
                org_list = r_idmorg['body']['LIST']
                xml_tree = ET.fromstring(org_list)
                if len(xml_tree) > 0:
                    DATE_LOOP = 'NO'
                    l_orginfo = []
                    for orginfo in xml_tree.iter('ORG'):
                        l_orglongnamestr = []
                        organnumber = orginfo.find('OrganNumber').text
                        organname = orginfo.find('OrganName').text
                        organparentno = orginfo.find('OrganParentNo').text
                        organupdate = orginfo.find('OrganUpdate').text
                        organcreate = orginfo.find('OrganCreate').text

                        organdisplayname = orginfo.find('OrganDisplayName').text
                        if organdisplayname is not None:
                            l_orglongname = organdisplayname.split('_')
                            orglevel = len(l_orglongname)
                            for index in range(orglevel):
                                if l_orglongname[index] == '融创中国':
                                    l_orglongname[index] = '融创集团'
                                    l_orglongnamestr.append('OU=' + l_orglongname[index])
                                else:
                                    l_orglongnamestr.append('OU=' + l_orglongname[index])
                            l_orglongnamestr.reverse()
                            orgdep = (','.join(l_orglongnamestr) + ',DC=testing,DC=local')
                        else:
                            orgdep = 'no idm organization'
                            orglevel = 0

                        organstatus = orginfo.find('OrganStatus').text
                        if organdisplayname is not None and organdisplayname.startswith('融创中国') \
                                and organstatus == 'Active':

                            dbcursor.execute(
                                'select organnumber, organname, organparentno, orgdep, orghandled from dic_idm_org '
                                'where organnumber = "%s" ' % organnumber)
                            rownum_idmorg = dbcursor.rowcount

                            if rownum_idmorg == 0:
                                pre_orgparentno = "no pre Organization Num"
                                pre_orgdep = "no pre Organization"
                                orghandled = 11
                            else:
                                obj_idmorg = dbcursor.fetchone()
                                pre_orgparentno = obj_idmorg[2]
                                pre_orgdep = obj_idmorg[3]
                                if organnumber == obj_idmorg[0] and obj_idmorg[4] == 11:
                                    orghandled = 11
                                elif organnumber == obj_idmorg[0] and organname != obj_idmorg[1] \
                                        and organparentno == pre_orgparentno:
                                    orghandled = 12
                                elif organnumber == obj_idmorg[0] and organname == obj_idmorg[1] \
                                        and organparentno != pre_orgparentno:
                                    orghandled = 13
                                elif organnumber == obj_idmorg[0] and organname == obj_idmorg[1] \
                                        and organparentno == pre_orgparentno and orgdep != pre_orgdep:
                                    orghandled = 5
                                else:
                                    orghandled = 3
                        else:
                            orghandled = 0
                            pre_orgparentno = "Error pre Organization Num"
                            pre_orgdep = "Error pre Organization"
                        orgobject = (organnumber, organname, organparentno, organupdate, organcreate,
                                     orgdep, orglevel, organstatus, pre_orgparentno, pre_orgdep, orghandled)
                        l_orginfo.append(orgobject)
                    dbcursor.executemany('replace into dic_idm_org(organnumber, organname, organparentno, organupdate, '
                                         'organcreate, orgdep, orglevel, organstatus, pre_orgparentno, pre_orgdep, '
                                         'orghandled) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', l_orginfo)
                    dbconn.commit()
                    infolog_org('IDM信息--查询时间：%s 至 %s，结果集当前分页：%s，变更组织数：%s' %
                                (begindatestr, enddatestr, NUM, len(xml_tree)))

                    if len(xml_tree) == 100:
                        NUM += 1
                    else:
                        infolog_org('IDM信息--没有更多的翻页数据')
                        NUM_LOOP = 'NO'

                else:
                    infolog_org('IDM信息--查询时间：%s 至 %s，没有查询到增量组织' % (begindatestr, enddatestr))
                    NUM_LOOP = 'NO'
                    begindatestr = enddatestr
                    enddatetime = datetime.strptime(enddatestr, '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=1)
                    enddatestr = datetime.strftime(enddatetime, '%Y-%m-%d %H:%M:%S.%f')
            else:
                errlog_org('IDM信息--组织查询接口出现错误')
                NUM_LOOP = 'NO'
                DATE_LOOP = 'NO'

except Exception as e:
    errlog_org(e)

finally:
    dbcursor.close()
    dbconn.close()
