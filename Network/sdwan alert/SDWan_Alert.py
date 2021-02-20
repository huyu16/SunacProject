#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
获取sdwan的告警，并通过微信转发给对应区域的同事
"""
from func import toweixin, secondstotime, sdwanquery, MysqlOper
import time
import datetime

dbconn = MysqlOper()

today = datetime.date.today()
cur_date = today.strftime("%Y-%m-%d %H:%M:%S")
end_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

try:
    resnum = dbconn.dbonequery('select count(0) from sdwan_alert where status = "triggering"')
    if resnum[0] == 0:
        min_datetime = dbconn.dbonequery('select max(createddate) from sdwan_alert where status = "finished" ')
    else:
        min_datetime = dbconn.dbonequery('select min(createddate) from sdwan_alert where status = "triggering" ')
    start_datetime = min_datetime[0].strftime("%Y-%m-%d %H:%M:%S")
    max_mod_datetime = dbconn.dbonequery('select max(lastmodifieddate) from sdwan_alert')
    mod_datetime = max_mod_datetime[0]
except Exception as e:
    print(e)
    start_datetime = cur_date
    mod_datetime = cur_date
    # start_datetime = '2021-01-26 00:00:00'
    # mod_datetime = '2021-01-26 00:00:00'
# 查询类型为1的故障信息，已有的信息不做覆盖
resvalue1 = sdwanquery(1, start_datetime, end_datetime)
print(resvalue1)
if len(resvalue1) > 0:
    resalert1 = []
    for objres1 in resvalue1:
        resnum1 = dbconn.dbonequery('select count(0) from sdwan_alert where alertid=%s and lastmodifieddate=%s',
                                    objres1[0], objres1[2])
        if resnum1[0] == 0:
            resalert1.append(objres1)
    # dbconn.dbmanyinsert('replace into sdwan_alert(alertid,createddate,lastmodifieddate,status,alertLevel,'
                        # 'textcontent,areaname,networkmgr,delaydate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', resalert1)
# 查询类型为2的恢复信息，已有的信息不做覆盖
resvalue2 = sdwanquery(2, start_datetime, end_datetime)
if len(resvalue2) > 0:
    resalert2 = []
    for objres2 in resvalue2:
        resnum2 = dbconn.dbonequery('select count(0) from sdwan_alert where alertid=%s and lastmodifieddate=%s',
                                    objres2[0], objres2[2])
        if resnum2[0] == 0:
            resalert2.append(objres2)
    # dbconn.dbmanyinsert('replace into sdwan_alert(alertid,createddate,lastmodifieddate,status,alertLevel,'
                        # 'textcontent,areaname,networkmgr,delaydate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', resalert2)

normal_alert = dbconn.dbmanyquery(
    'select alertid,createddate,lastmodifieddate,status,alertlevel,textContent,areaname,networkmgr '
    'from sdwan_alert where lastmodifieddate > %s order by lastmodifieddate', mod_datetime)
delay_alert = dbconn.dbmanyquery(
    'select alertid,createddate,lastmodifieddate,status,alertlevel,textContent,areaname,networkmgr '
    'from sdwan_alert where status = "triggering" and now() > SUBDATE(createddate,interval -delaydate day) '
    'order by lastmodifieddate')
print(normal_alert)
print(delay_alert)
if len(normal_alert) > 0:
    for objnormal in normal_alert:
        # weixinuser = objnormal[7] + '|wangar1|yangyc1|huy33'
        weixinuser = 'wangar1|yangyc1|huy33'
        if objnormal[3] == "triggering":
            weixindata = '\n【告警区域】' + objnormal[6] + '\n【告警内容】' + objnormal[5]
            print(weixindata)
            # toweixin(weixinuser, '【故障告警-SDWAN】', weixindata)
        elif objnormal[3] == "finished":
            sectime = (objnormal[2] - objnormal[1]).seconds
            weixindata = '\n【告警区域】' + objnormal[6] + \
                         '\n【告警内容】' + objnormal[5] + \
                         '\n【告警持续时间】' + secondstotime(sectime) + \
                         '\n【故障恢复时间】' + str(objnormal[2])
            print(weixindata)
            # toweixin(weixinuser, '【恢复告警-SDWAN】', weixindata)
        else:
            pass
if len(delay_alert) > 0:
    for objdealy in delay_alert:
        # weixinuser = objdealy[7] + '|wangar1|yangyc1|huy33'
        weixinuser = 'wangar1|yangyc1|huy33'
        weixindata = '\n【延时告警】请注意！此告警已延时超过一天' + '\n【告警区域】' + objdealy[6] + '\n【告警内容】' + objdealy[5]
        print(weixindata)
        # toweixin(weixinuser, '【故障告警-SDWAN】', weixindata)
        # dbconn.dbonemod('update sdwan_alert set delaydate = delaydate+1 where alertid = %s', objdealy[0])

dbconn.dbclose()
