#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .logger import infolog_user, errlog_user, debuglog_user
import xml.etree.ElementTree as ET
from zeep import Client
from zeep.plugins import HistoryPlugin
from datetime import datetime, timedelta
import pymysql
from ldap3 import Server, Connection, SUBTREE

timestr = datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
idmid = 'AD_SUNAC_300_' + timestr
history = HistoryPlugin()
WSDL_URL = 'http://esbqas.sunac.com.cn:8001/WP_SUNAC/APP_PUBLIC_SERVICES/Proxy_Services/TA_IDM/PUBLIC_SUNAC_300_queryIdmUserData_PS?wsdl'
INITIAL_TIME = datetime.strptime('2020-12-16 00:00:00.000', '%Y-%m-%d %H:%M:%S.%f')
CURRENT_DATE = datetime.today()

try:
    # 绑定Mysql数据库
    dbconn = pymysql.connect(
        host='10.4.64.2',
        user='aduser',
        passwd='ADuser@123',
        db='ad',
        charset='utf8')
    dbcursor = dbconn.cursor()

    dbcursor.execute('select count(0) from dic_idm_user')
    rownum = dbcursor.fetchone()[0]
    if rownum == 0:
        begindatetime = INITIAL_TIME + timedelta(seconds=1)
        enddatetime = begindatetime + timedelta(days=1)
        begindatestr = datetime.strftime(begindatetime, '%Y-%m-%d %H:%M:%S.%f')
        enddatestr = datetime.strftime(enddatetime, '%Y-%m-%d %H:%M:%S.%f')
    else:
        dbcursor.execute('SELECT max(userupdate) from dic_idm_user')
        begindatetime = dbcursor.fetchone()[0] + timedelta(seconds=1)
        enddatetime = begindatetime + timedelta(days=1)
        begindatestr = datetime.strftime(begindatetime, '%Y-%m-%d %H:%M:%S.%f')
        enddatestr = datetime.strftime(enddatetime, '%Y-%m-%d %H:%M:%S.%f')
    # 没有查询到数据，增加日期继续查找
    DATE_LOOP = 'YES'
    while datetime.strptime(begindatestr, '%Y-%m-%d %H:%M:%S.%f') < CURRENT_DATE and DATE_LOOP == 'YES':
        NUM = 1
        NUM_LOOP = 'YES'
        # 最大获取900条的数据，循环9次
        while NUM <= 100 and NUM_LOOP == 'YES':
            client = Client(wsdl=WSDL_URL, plugins=[history])
            querydto_type = client.get_type('ns0:queryDto')
            header_type = client.get_type('ns2:Header')
            querydto = querydto_type(beginDate=begindatestr, endDate=enddatestr,
                                     pageNo=NUM, pageRowNo='100', systemID='Sunac_IDMUser')
            header = header_type(BIZTRANSACTIONID=idmid, COUNT='', CONSUMER='',
                                 SRVLEVEL='', ACCOUNT='idmadmin', PASSWORD='idmpass')

            r_idmuser = client.service.PUBLIC_SUNAC_300_queryIdmUserData(queryDto=querydto,
                                                                         _soapheaders={'parameters2': header})
            debuglog_user(history.last_sent)
            debuglog_user(history.last_received)

            if r_idmuser['body']['HEADER']['RESULT'] == '0':
                user_list = r_idmuser['body']['LIST']
                xml_tree = ET.fromstring(user_list)
                if len(xml_tree) > 0:
                    DATE_LOOP = 'NO'
                    l_userinfo = []
                    for userinfo in xml_tree.iter('USER'):
                        l_userorgstr = []
                        userid = userinfo.find('UserLogin').text
                        username = userinfo.find('Username').text
                        userdeptno = userinfo.find('UserDeptNo').text

                        userorginfo = userinfo.find('UserOrgDisplayName').text
                        if userorginfo is not None:
                            l_userorg = userorginfo.split('_')
                            for index in range(len(l_userorg)):
                                if l_userorg[index] == '融创中国':
                                    l_userorg[index] = '融创集团'
                                    l_userorgstr.append('OU=' + l_userorg[index])
                                else:
                                    l_userorgstr.append('OU=' + l_userorg[index])
                            l_userorgstr.reverse()
                            userorg = (','.join(l_userorgstr) + ',DC=testing,DC=local')
                        else:
                            userorg = 'no idm organization'

                        userupdate = userinfo.find('UserUpdate').text
                        usercreate = userinfo.find('UserCreate').text
                        useremptype = userinfo.find('UserEmpType').text
                        userstatus = userinfo.find('UserStatus').text
                        userexpirydate = userinfo.find('UserExpiryDate').text

                        if userorginfo is not None and userorginfo.startswith('融创中国') \
                                and userstatus == 'Active' and useremptype == 'Full-Time':
                            userhandled = 11
                        else:
                            userhandled = 0
                        t_userobj = (userid, username, userdeptno, userorg, userupdate, usercreate,
                                     useremptype, userstatus, userexpirydate, userhandled)
                        l_userinfo.append(t_userobj)
                    dbcursor.executemany(
                        'replace into dic_idm_user(userid,username,userdeptno,userorg,userupdate,'
                        'usercreate,useremptype,userstatus,userexpirydate,userhandled) '
                        'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        l_userinfo)
                    dbconn.commit()
                    infolog_user('IDM信息--查询时间：%s 至 %s，结果集当前分页：%s，新增用户数：%s' %
                                 (begindatestr, enddatestr, NUM, len(xml_tree)))
                    if len(xml_tree) == 100:
                        NUM += 1
                    else:
                        infolog_user('IDM信息--没有更多的翻页数据')
                        NUM_LOOP = 'NO'
                else:
                    infolog_user('IDM信息--查询时间：%s 至 %s，没有查询到增量用户' % (begindatestr, enddatestr))
                    NUM_LOOP = 'NO'
                    begindatestr = enddatestr
                    enddatetime = datetime.strptime(enddatestr, '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=1)
                    enddatestr = datetime.strftime(enddatetime, '%Y-%m-%d %H:%M:%S.%f')
            else:
                errlog_user('IDM信息--用户查询接口出现错误')
                NUM_LOOP = 'NO'
                DATE_LOOP = 'NO'

except Exception as e:
    errlog_user(e)

finally:
    dbcursor.close()
    dbconn.close()
