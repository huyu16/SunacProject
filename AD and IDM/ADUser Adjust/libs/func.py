#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper
from libs.logger import errlog_org

def incdate(incdate,curdate,inctype):
    try:
        dbconn = MysqlOper()
        if incdate < curdate:
            inc_flag = incdate
        else:
            inc_flag = curdate
        dbconn.dbonemod('update idm_inc_flag set inc_datetime=%s where inc_type=%s', inc_flag, inctype)
    except Exception as e:
        errlog_org(e)
    finally:
        dbconn.dbclose()