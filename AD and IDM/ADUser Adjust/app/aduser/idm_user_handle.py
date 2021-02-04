#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper
from libs.logger import infolog_user, errlog_user


def area_user_handle(v_area, levelnum):
    dbconn = MysqlOper()

    userhandlenum = dbconn.dbonequery('select count(0) from idm_user_handle where userareaid = %s', v_area)
    if userhandlenum[0] == 0:
        user_basic = dbconn.dbmanyquery('select userid, username, userdeptno, userorg, userupdate, '
                                        'usercreate, useremptype, userstatus, userareaid '
                                        'from idm_user_data where userareaid = %s', v_area)
    else:
        user_incdate = dbconn.dbonequery('select max(userupdate) from idm_user_handle '
                                         'where userareaid = %s', v_area)
        user_basic = dbconn.dbmanyquery('select userid, username, userdeptno, userorg, userupdate, '
                                        'usercreate, useremptype, userstatus, userareaid from idm_user_data '
                                        'where userupdate > %s and userareaid = %s', user_incdate[0], v_area)

    if len(user_basic) > 0:
        l_userinfo = []
        for userinfo in user_basic:
            l_userorgou = []
            userid = userinfo[0]
            username = userinfo[1]
            userdeptno = userinfo[2]
            userupdate = userinfo[4]
            usercreate = userinfo[5]
            useremptype = userinfo[6]
            userstatus = userinfo[7]
            userareaid = userinfo[8]

            l_userorg = userinfo[3].split('_')
            v_userorglevel = len(l_userorg)
            if v_userorglevel >= levelnum:
                userorglevel = levelnum
            else:
                userorglevel = v_userorglevel
            for index in range(userorglevel):
                if l_userorg[index] == '融创中国':
                    l_userorg[index] = '融创集团'
                    l_userorgou.append('OU=' + l_userorg[index])
                else:
                    l_userorgou.append('OU=' + l_userorg[index])
            l_userorgou.reverse()
            userorg = (','.join(l_userorgou) + ',DC=testing,DC=local')
            # 判断条件不够，可以加上 用户如果没有变化 就不需要
            if userstatus == 'Active' and useremptype == 'Full-Time':
                res_userhandle = dbconn.dbonequery('select userid, userorg, userhandled from idm_user_handle '
                                                   'where userid = %s', userid)
                if res_userhandle is not None and res_userhandle[1] == userorg and res_userhandle[2] in (1, 2):
                    userhandled = 7
                else:
                    userhandled = 11
            else:
                userhandled = 0
            t_userobj = (userid, username, userdeptno, userorg, userupdate,
                         usercreate, useremptype, userstatus, userareaid, userhandled)
            l_userinfo.append(t_userobj)
        res_insert = dbconn.dbmanyinsert('replace into idm_user_handle(userid,username,userdeptno,userorg,'
                                         'userupdate,usercreate,useremptype,userstatus,userareaid,userhandled) '
                                         'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', l_userinfo)
        if res_insert:
            infolog_user('IDM信息--区域编号"%s" 已处理用户原始数据信息：%s条' % (v_area, len(user_basic)))
    else:
        infolog_user('IDM信息--区域编号"%s" 没有新的组织需要做处理' % v_area)

    dbconn.dbclose()
