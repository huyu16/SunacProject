#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import json
import time
import pymysql
import requests
import re


def md5encode(secstr):
    # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    m = hashlib.md5(secstr.encode(encoding='utf-8'))
    return m.hexdigest()


def toweixin(v_touser, v_subject, v_message):
    agentid = '1000006'
    corpid = 'ww8b9c73d119c3b4a8'
    corpsecret = 'HycqSE0dEgnjpABoKA-Lw0D9-oulzavdCSmVl4AsoHg'
    url = 'https://qyapi.weixin.qq.com'
    token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
    req = requests.get(token_url)
    token = req.json()['access_token']
    send_url = '%s/cgi-bin/message/send?access_token=%s' % (url, token)
    values = {
        "touser": v_touser,
        "msgtype": 'text',
        "agentid": agentid,
        "text": {'content': v_subject + v_message},
        "safe": 0
    }
    reqdata = json.dumps(values)
    requests.post(url=send_url, data=reqdata)


def secondstotime(v_second):
    delta = datetime.timedelta(seconds=v_second)
    totime = (str(delta).split('.')[0])
    return totime


class MysqlOper:
    def __init__(self):
        self.host = '10.4.64.2'
        self.user = 'networkuser'
        self.passwd = 'NETWORKuser@123'
        self.dbname = 'network'
        self.charset = 'utf8'
        self.dbconn = self.dbconnect()

        if self.dbconn:
            self.dbcursor = self.dbconn.cursor()

    def dbconnect(self):
        mysqlconn = ''
        mysqlconn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    passwd=self.passwd,
                                    db=self.dbname,
                                    charset=self.charset)
        return mysqlconn

    def dbclose(self):
        if self.dbconn:
            if self.dbcursor:
                self.dbcursor.close()
            if self.dbconn:
                self.dbconn.close()

    def dbmanyquery(self, sql, *args):
        """
        执行多行查询语句
        """
        resmany = ''
        if self.dbconn:
            self.dbcursor.execute(sql, args)
            resmany = self.dbcursor.fetchall()
        return resmany

    def dbonequery(self, sql, *args):
        resone = ''
        if self.dbconn:
            self.dbcursor.execute(sql, args)
            resone = self.dbcursor.fetchone()
        return resone

    def dbmanyinsert(self, sql, l_value):
        if self.dbconn:
            try:
                self.dbcursor.executemany(sql, l_value)
                self.dbconn.commit()
            except Exception as e:
                print(e)
                self.dbconn.rollback()

    def dbonemod(self, sql, *args):
        if self.dbconn:
            try:
                self.dbcursor.execute(sql, args)
                self.dbconn.commit()
            except Exception as e:
                self.dbconn.rollback()


def sdwanquery(typenum, startdate, enddate):
    includestr = ['CPE Pending', 'Connection PacketLoss Ratio High']
    l_alert = []

    timestamp = time.time()
    cur_timestamp = int(timestamp)
    str_sign = f"alertType={typenum}&e={enddate}&page=0&s={startdate}&size=30&timestamp={cur_timestamp}&v=2_1_2" \
               f"&secretKey=81947cba9b38481d96023a82dea54e58"
    v_sign = md5encode(str_sign).upper()
    req_param = f"alertType={typenum}&e={enddate}&page=0&s={startdate}&size=30&timestamp={cur_timestamp}&v=2_1_2"
    req_url = f"http://user.bestsdwan.com/external/api/alert/alertList?{req_param}"
    header = {
        # "Content-type": 'application/json; charset=utf-8',
        "token": "d61a3676ad0f4490b7ff54db22e28052",
        "sign": v_sign
    }
    r = requests.get(url=req_url, headers=header)
    resvalue = r.json()['data']

    for objinfo in resvalue:
        if objinfo['status'] in ['finished', 'triggering'] \
                and objinfo['businessMetric']['moduleAndAction'] in includestr:
            alertid = objinfo['id']
            createddate = objinfo['createdDate']
            lastmodifieddate = objinfo['lastmodifiedDate']
            status = objinfo['status']
            alertlevel = objinfo['alertLevel']
            textContent = objinfo['textContent']
            alertparm = toarea(objinfo['moduleName'])
            areaname = '融创' + alertparm[0]
            networkmgr = alertparm[1]

            curdate = datetime.date.today()
            lastdate = datetime.datetime.strptime(createddate, '%Y-%m-%dT%H:%M:%S.%f').date()
            daynum = (curdate - lastdate).days+1

            t_alertinfo = (
                alertid, createddate, lastmodifieddate, status, alertlevel, textContent, areaname, networkmgr, daynum)
            l_alert.append(t_alertinfo)
    return l_alert


def toarea(modulename):
    alertparm = ''
    areadbconn = pymysql.connect(
        host='10.4.64.2',
        user='aduser',
        passwd='ADuser@123',
        db='ad',
        charset='utf8')
    areadbcursor = areadbconn.cursor()
    areadbcursor.execute('select areaname,sdwancode,networkmgr from sum_inf_area where parentid = 0')
    t_sdwancode = areadbcursor.fetchall()
    for objsdwan in t_sdwancode:
        if re.search(objsdwan[1], modulename):
            sdwanname = objsdwan[0]
            networkmgr = objsdwan[2]
            alertparm = (sdwanname, networkmgr)
            break
        else:
            alertparm = ('无匹配区域', '无管理者')
    areadbcursor.close()
    areadbconn.close()
    return alertparm

