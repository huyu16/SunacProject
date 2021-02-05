#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, ssl
ssl._create_default_https_context = ssl._create_unverified_context

authurl = "https://10.4.0.205/shterm/api/authenticate"
userurl = "https://10.4.0.205/shterm/api/user"
devurl = "https://10.4.0.205/shterm/api/resGroup/listOutterDevs"
resgroupurl = "https://10.4.0.205/shterm/api/resGroup"
list_iditem = []

def getToken():
    header = {'Content-type': 'application/json; charset=utf-8'}
    data = json.dumps({'username':'admin', 'password':'RIS@sunac2019'})
    auth = requests.post(authurl, data, headers=header,verify=False)
    return auth.json()['ST_AUTH_TOKEN']

def getOff(authtoken):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    httpcode = requests.delete(authurl,headers=header,verify=False)
    if httpcode.status_code == 204:
        print('注销成功')
    else:
        print('注销失败')

def getDevinf(authtoken,v_groupid1):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    dev_inf_url = 'https://10.4.0.205/shterm/api/resGroup/listOutterDevs/' + v_groupid1 + '?size=50&search=生产-'
    dev_inf_request = requests.get(dev_inf_url, headers=header, verify=False)
    return dev_inf_request.json()

def getResGroup(authtoken):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    dev_inf_url = resgroupurl + '?search=信息-生产服务器组'
    dev_inf_request = requests.get(dev_inf_url, headers=header, verify=False)
    return dev_inf_request.json()

def putResGroup(authtoken,v_groupid2,v_array_id):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    data = json.dumps(v_array_id)
    put_group_url = 'https://10.4.0.205/shterm/api/resGroup/relateDevs/' + v_groupid2
    put_group_request = requests.put(put_group_url, data, headers=header, verify=False)
    print(put_group_request.text)

if __name__ == "__main__":
    auth_token = getToken()
    resgroup_inf = getResGroup(auth_token)
    resgroup_id = str(resgroup_inf["content"][0]['id'])
    dev_inf = getDevinf(auth_token,resgroup_id)
    print(len(dev_inf['content']))
    for dic_dev in (dev_inf['content']):
        dic_id = {}
        dic_id['id'] = dic_dev['id']
        list_iditem.append(dic_id)
    putResGroup(auth_token,resgroup_id,list_iditem)

    getOff(auth_token)