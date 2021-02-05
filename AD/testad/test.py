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


