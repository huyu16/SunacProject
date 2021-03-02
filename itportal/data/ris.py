#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import urllib3

# 关闭ssl警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 导入ssl模块，忽略ssl证书
# ssl._create_default_https_context = ssl._create_unverified_context

AUTHURL = "https://10.4.0.205/shterm/api/authenticate"
USERURL = "https://10.4.0.205/shterm/api/user"
DEVURL = "https://10.4.0.205/shterm/api/resGroup/listOutterDevs"
RESGROUPURL = "https://10.4.0.205/shterm/api/resGroup"


def gettoken():
    header = {'Content-type': 'application/json; charset=utf-8'}
    data = json.dumps({'username': 'admin', 'password': 'RIS@sunac2019'})
    auth = requests.post(AUTHURL, data, headers=header, verify=False)
    return auth.json()['ST_AUTH_TOKEN']


def getoff(authtoken):
    header = {
        'Content-type': 'application/json; charset=utf-8',
        'st-auth-token': authtoken
    }
    httpcode = requests.delete(AUTHURL, headers=header, verify=False)
    if httpcode.status_code == 204:
        print('注销成功')
    else:
        print('注销失败')


def get_resgroup(authtoken):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            'st-auth-token': authtoken
        }
    dev_inf_url = RESGROUPURL + '?search=信息-生产服务器组'
    dev_inf_request = requests.get(dev_inf_url, headers=header, verify=False)
    return dev_inf_request.json()


def get_devinf(authtoken):
    header = {
        'Content-type': 'application/json; charset=utf-8',
        'st-auth-token': authtoken
    }
    dev_inf_url = 'https://10.4.0.205/shterm/api/resGroup/listDevs/280?size=2000'
    dev_inf_request = requests.get(dev_inf_url, headers=header, verify=False)
    return dev_inf_request.json()


def get_extuser(authtoken):
    header = {
        'Content-type': 'application/json; charset=utf-8',
        'st-auth-token': authtoken
    }
    extuser_inf_url = 'https://10.4.0.205/shterm/api/user?state=0&role.id=102&size=2000'
    extuser_inf_request = requests.get(extuser_inf_url, headers=header, verify=False)
    return extuser_inf_request.json()


