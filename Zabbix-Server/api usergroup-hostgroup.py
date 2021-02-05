#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,json

headers = {'Content-Type': 'application/json-rpc'}
server_ip = '10.4.64.64'

url = 'http://%s/zabbix/api_jsonrpc.php' %server_ip

def getToken():
    username = 'Admin'
    passwd = 'zabbix'
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": passwd
        },
        "id": 1
    }

    request = requests.post(url=url, headers=headers, data=json.dumps(data))
    dict = json.loads(request.text)
    return dict['result']

def getusergroup():
    data = {
            "jsonrpc": "2.0",
            "method": "usergroup.get",
            "params": {
                "output": "extend",
                "status": 0
            },
            "auth": token_num,
            "id": 2
        }
    request = requests.post(url=url, headers=headers, data=json.dumps(data))
    dict = json.loads(request.text)
    print(dict)

if __name__ == "__main__":
    token_num = getToken()
    usergroupdata = getusergroup()
    print(usergroupdata)

