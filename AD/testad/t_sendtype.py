#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


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

if __name__ == '__main__':
    toweixin('huy33|wangar1', '【网络告警-SDWAN】', '\n【告警区域】：融创西南区域集团\n【告警内容】：[SLA] Customer:融创全国组网-已签约, Site: 北京集团RC-BJ-19123001[3], Connection: 西南区域平台专业公司+财务共享中心 DXN-CWGX-20111101_WAN--北京集团RC-BJ-19123001_CUWAN [label 235728, star 3] DOWN at 2021-01-17 18:49:21')