#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import os
import json
import logging

# logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s, %(filename)s, %(levelname)s, %(message)s',datefmt = '%a, %d %b %Y %H:%M:%S',filename = os.path.join('/acdata/zabbix/log','weixin.log'),filemode = 'a')
corpid = 'ww8b9c73d119c3b4a8'  # 企业ID
appsecret = 'eBjBxoicYwbwlX2SmmT2307-CoprVrAX9AamhIxisdc'  # secret
agentid = 1000003  # AgentID
# 获取accesstoken
token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
req = requests.get(token_url)
accesstoken = req.json()['access_token']

# 发送消息
msgsend_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken

touser = sys.argv[1]
subject = sys.argv[2]
# toparty='3|4|5|6'
message = sys.argv[3]

params = {
    "touser": touser,
    #       "toparty": toparty,
    "msgtype": "text",
    "agentid": agentid,
    "text": {
        "content": message
    },
    "safe": 0
}

req = requests.post(msgsend_url, data=json.dumps(params))

logging.warning('sendto:' + touser + ';;subject:' + subject + ';;message:' + message)
