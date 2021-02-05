#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper, idmquery
from datetime import datetime, timedelta
from libs.logger import errlog_user, infolog_user
import xml.etree.ElementTree as Et
from libs.func import incdate

CURRENT_DATE = datetime.today()
timestr = datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
idmid = 'AD_SUNAC_300_' + timestr
WSDL_URL = "http://esb.sunac.com.cn:8002/WP_SUNAC/APP_PUBLIC_SERVICES" \
           "/Proxy_Services/TA_IDM/PUBLIC_SUNAC_300_queryIdmUserData_PS?wsdl"
# WSDL_URL = "http://esbqas.sunac.com.cn:8001/WP_SUNAC/APP_PUBLIC_SERVICES" \
#                "/Proxy_Services/TA_IDM/PUBLIC_SUNAC_300_queryIdmUserData_PS?wsdl"
# SYSTEMID = 'Sunac_IDMUser'
SYSTEMID = 'Sunac_ADQZ_USR'

dbconn = MysqlOper()
# IDM一天的增量查询，确定开始和结束时间。
inc_begindate = dbconn.dbonequery('select inc_datetime from idm_inc_flag where inc_type="user" ')
begintime = datetime.strftime(inc_begindate[0], '%Y-%m-%d %H:%M:%S.%f')
inc_enddate = inc_begindate[0] + timedelta(days=2)
endtime = datetime.strftime(inc_enddate, '%Y-%m-%d %H:%M:%S.%f')

try:
    NUM = 1
    NUM_LOOP = 'YES'
    # 查询到的增量 最多循环999页，每页100条数据，如果查询到的当前页小于100条 停止页面循环，如果等于100条，继续查询下一页
    while NUM <= 999 and NUM_LOOP == 'YES':
        residmuser = idmquery(WSDL_URL, begintime, endtime, NUM, SYSTEMID, idmid, 'idmuser')
        print(residmuser)
        if residmuser['body']['HEADER']['RESULT'] == '0':
            # XML中不允许有&,否则会解析失败
            user_list_old = residmuser['body']['LIST']
            user_list = user_list_old.replace("&", "及")
            xml_tree = Et.fromstring(user_list)
            if len(xml_tree) > 0:
                l_userinfo = []
                for userinfo in xml_tree.iter('USER'):
                    userid = userinfo.find('UserLogin').text
                    username = userinfo.find('Username').text
                    userdeptno = userinfo.find('UserDeptNo').text
                    userorg = userinfo.find('UserOrgDisplayName').text
                    userupdate = userinfo.find('UserUpdate').text
                    usercreate = userinfo.find('UserCreate').text
                    useremptype = userinfo.find('UserEmpType').text
                    userstatus = userinfo.find('UserStatus').text
                    t_userobj = (userid, username, userdeptno, userorg, userupdate, usercreate, useremptype, userstatus)
                    l_userinfo.append(t_userobj)
                res_insert = dbconn.dbmanyinsert('replace into idm_user_data(userid,username,userdeptno,userorg,'
                                                 'userupdate, usercreate,useremptype,userstatus) '
                                                 'values (%s,%s,%s,%s,%s,%s,%s,%s)', l_userinfo)
                if res_insert:
                    infolog_user('IDM信息--查询时间：%s 至 %s，结果集当前分页：%s，新增用户数：%s' %
                                 (str(inc_begindate), str(inc_enddate), NUM, len(xml_tree)))
                    if len(xml_tree) == 100:
                        NUM += 1
                    else:
                        infolog_user('IDM信息--没有更多的翻页数据')
                        NUM_LOOP = 'NO'
                        # 判断增量的日期，插入增量标志作为下次增量查询的开始时间
                        incdate(inc_enddate, CURRENT_DATE, 'user')
                else:
                    errlog_user('IDM信息--组织插入失败')
            else:
                infolog_user('IDM信息--查询时间：%s 至 %s，没有查询到增量用户' % (str(inc_begindate), str(inc_enddate)))
                NUM_LOOP = 'NO'
                # 判断增量的日期，插入增量标志作为下次增量查询的开始时间
                incdate(inc_enddate, CURRENT_DATE, 'user')
        else:
            errlog_user('IDM信息--用户查询接口出现错误')
            NUM_LOOP = 'NO'
except Exception as e:
    errlog_user(e)
finally:
    # 关闭数据库连接
    dbconn.dbclose()
