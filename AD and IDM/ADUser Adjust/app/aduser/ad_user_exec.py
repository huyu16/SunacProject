#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.logger import infolog_user, errlog_user
from libs.connect import AdOper, MysqlOper


def area_user_exec(v_area):
    dbconn = MysqlOper()
    adconn = AdOper()

    processed_user = dbconn.dbmanyquery('select userid,userorg from idm_user_handle '
                                        'where userhandled > 9 and userareaid = %s', v_area)
    for userobj in processed_user:
        adfilterstr = f'(&(objectClass=person)(sAMAccountName={userobj[0].lower()})(!(userAccountControl=514)))'
        adquery = adconn.adquery('ou=融创集团,dc=testing,dc=local', adfilterstr)
        if adquery:
            for aduserobj in adconn.adconn.response:
                pre_userorg = aduserobj['dn']
                l_userorg = pre_userorg.split(',')
                userobjcn = l_userorg[0]
                userobjou = ','.join(l_userorg[1:])
                if userobjou != userobj[1]:
                    res_admodify = adconn.admove(pre_userorg, userobjcn, userobj[1])
                    if res_admodify:
                        dbconn.dbonemod('update idm_user_handle set pre_userorg=%s,userhandled=1 '
                                        'where userid = %s', pre_userorg, userobj[0])
                        infolog_user('AD信息--已移动到新OU的用户：%s' % (userobj[0]))
                    else:
                        dbconn.dbonemod('update idm_user_handle set pre_userorg=%s,userhandled=10 '
                                        'where userid=%s', pre_userorg, userobj[0])
                        errlog_user('AD信息--移动OU失败的用户：%s' % (userobj[0]))
                else:
                    dbconn.dbonemod('update idm_user_handle set pre_userorg=%s,userhandled=2 '
                                    'where userid = %s', pre_userorg, userobj[0])
                    infolog_user('AD信息--已存在的用户：%s' % (userobj[0]))
        else:
            pre_userorg = 'no ad user'
            dbconn.dbonemod('update idm_user_handle set pre_userorg=%s,userhandled=0 '
                            'where userid = %s', pre_userorg, userobj[0])
            errlog_user('AD信息--没有创建的无效用户：%s' % (userobj[0]))

    adconn.adclose()
    dbconn.dbclose()


if __name__ == '__main__':
    area_user_exec('000104')
