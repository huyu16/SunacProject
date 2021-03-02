#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zeep import Client
from overview.models import UserExpire
from django.db.models import Max
from datetime import datetime
import xml.etree.ElementTree as Et
from data.common import MysqlOper


def inc_tempuser():
    dbconn = MysqlOper()

    CURRENT_DATE = datetime.today()
    timestr = datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    idmid = 'AD_SUNAC_300_' + timestr

    WSDL_URL = "http://esb.sunac.com.cn:8002/WP_SUNAC/APP_PUBLIC_SERVICES/Proxy_Services/TA_IDM" \
               "/PUBLIC_SUNAC_300_queryIdmUserData_PS?wsdl"
    SYSTEMID = 'Sunac_ADLS_USR'
    NUM = 1
    NUM_LOOP = 'YES'

    object_max_dbtime = UserExpire.objects.aggregate(Max('updatetime'))
    begintime = datetime.strftime(object_max_dbtime['updatetime__max'], '%Y-%m-%d %H:%M:%S.%f')

    while NUM <= 999 and NUM_LOOP == 'YES':
        client = Client(wsdl=WSDL_URL)
        querydto_type = client.get_type('ns0:queryDto')
        header_type = client.get_type('ns2:Header')
        querydto = querydto_type(beginDate=begintime, endDate=CURRENT_DATE,
                                 pageNo=NUM, pageRowNo='100', systemID=SYSTEMID)
        header = header_type(BIZTRANSACTIONID=idmid, COUNT='', CONSUMER='',
                             SRVLEVEL='', ACCOUNT='idmadmin', PASSWORD='idmpass')
        residmquery = client.service.PUBLIC_SUNAC_300_queryIdmUserData(queryDto=querydto,
                                                                       _soapheaders={'parameters2': header})

        if residmquery['body']['HEADER']['RESULT'] == '0':
            user_list_old = residmquery['body']['LIST']
            user_list = user_list_old.replace("&", "及")
            xml_tree = Et.fromstring(user_list)
            if len(xml_tree) > 0:
                l_userinfo = []
                for userinfo in xml_tree.iter('USER'):
                    userid = userinfo.find('UserLogin').text
                    username = userinfo.find('Username').text
                    company = userinfo.find('UserAddress').text
                    phone = userinfo.find('Mobile').text
                    email = userinfo.find('Email').text
                    state = userinfo.find('UserStatus').text
                    expiretime = userinfo.find('UserExpiryDate').text
                    updatetime = userinfo.find('UserUpdate').text
                    createtime = userinfo.find('UserCreate').text
                    usertype = userinfo.find('UserEmpType').text
                    t_userobj = (userid, username, company, phone, email, state, expiretime, updatetime, createtime,
                                 usertype)
                    l_userinfo.append(t_userobj)
                dbconn.dbmanyinsert('replace into overview_userexpire (userid,username,company,phone,email,state,'
                                    'expiretime,updatetime,createtime,usertype) '
                                    'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                    l_userinfo)

                if len(xml_tree) == 100:
                    NUM += 1
                else:
                    NUM_LOOP = 'NO'
            else:
                NUM_LOOP = 'NO'
        else:
            NUM_LOOP = 'NO'

    dbconn.dbclose()
