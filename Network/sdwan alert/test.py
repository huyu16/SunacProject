#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, time
from func import md5encode, toweixin, millitotime
import requests
import pymysql

dbconn = pymysql.connect(
    host='10.4.64.2',
    user='networkuser',
    passwd='NETWORKuser@123',
    db='network',
    charset='utf8')
dbcursor = dbconn.cursor()

timestamp = time.time()
cur_timestamp = int(timestamp)
start_datetime = '2021-01-29 15:05:54'
end_datetime = '2021-01-29 18:00:00'

str_sign = f"alertType=2&e={end_datetime}&page=0&s={start_datetime}&size=30&timestamp={cur_timestamp}" \
           f"&v=2_1_2&secretKey=81947cba9b38481d96023a82dea54e58"

v_sign = md5encode(str_sign).upper()

req_param = f"alertType=2&e={end_datetime}&page=0&s={start_datetime}&size=30&timestamp={cur_timestamp}&v=2_1_2"
req_url = f"http://user.bestsdwan.com/external/api/alert/alertList?{req_param}"

header = {
    # "Content-type": 'application/json; charset=utf-8',
    "token": "d61a3676ad0f4490b7ff54db22e28052",
    "sign": v_sign
}

r = requests.get(url=req_url, headers=header)
print(r.text)
resvalue = r.json()['data']

inertvalue = []
for objinf in resvalue:
    print(objinf)
#     if objinf['version'] == 1:
#         alertid = objinf['id']
#         createdDate = objinf['createdDate']
#         lastmodifiedDate = objinf['lastmodifiedDate']
#         ruleId = objinf['ruleId']
#         ruleName = objinf['ruleName']
#         triggercount = objinf['triggercount']
#         intervalMinute = objinf['intervalMinute']
#         alertstatus = objinf['status']
#         alertLevel = objinf['alertLevel']
#         alertModule = objinf['alertModule']
#         durationMilli = objinf['durationMilli']
#         module = objinf['businessMetric']['module']
#         moduleValue = objinf['businessMetric']['moduleValue']
#         moduleName = objinf['businessMetric']['moduleName']
#         moduleAndAction = objinf['businessMetric']['moduleAndAction']
#         htmlContent = objinf['businessMetric']['htmlContent']
#         textContent = objinf['businessMetric']['textContent']
#         alertDisabled = objinf['businessMetric']['alertDisabled']
#         alarmRecoveryKey = objinf['businessMetric']['alarmRecoveryKey']
#         alarmKey = objinf['businessMetric']['alarmKey']
#         recoverable = objinf['businessMetric']['recoverable']
#         recovery = objinf['businessMetric']['recovery']
#         alertinfo = (alertid, createdDate, lastmodifiedDate, ruleId, ruleName, triggercount, intervalMinute,
#                       alertstatus, alertLevel, alertModule, durationMilli, module, moduleValue, moduleName,
#                       moduleAndAction, htmlContent, textContent, alertDisabled, alarmRecoveryKey, alarmKey,
#                       recoverable, recovery)
#
#         inertvalue.append(alertinfo)
#
# dbcursor.executemany('insert into sdwan_alert values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', inertvalue)
# dbconn.commit()


dbcursor.close()
dbconn.close()


