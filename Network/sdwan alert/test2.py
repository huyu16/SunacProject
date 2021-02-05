#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from func import md5encode
import requests
from func import toweixin, secondstotime, sdwanquery, toarea, MysqlOper

dbconn = MysqlOper()

mod_datetime = datetime.datetime.strptime('2021-01-29 00:00:00', '%Y-%m-%d %H:%M:%S')
print(type(mod_datetime))

normal_alert = dbconn.dbmanyquery(
    'select alertid,createddate,lastmodifieddate,status,alertlevel,textContent,areaname,networkmgr '
    'from sdwan_alert where lastmodifieddate > %s order by lastmodifieddate', mod_datetime)

print(normal_alert)

# for t in res:
#     print(t[0])
#     s = (t[2] - t[1]).seconds
#     print(secondstotime(s))
#
# curdate = datetime.date.today()
# print(curdate)
#
# datestr = '2021-01-29T18:29:49.853'
#
# lastdate = datetime.datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S.%f').date()
# print(lastdate)
#
# daynum = (curdate - lastdate).days+1
#
# print(daynum)
#
#
#
