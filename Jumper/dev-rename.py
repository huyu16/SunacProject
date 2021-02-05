#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, ssl
ssl._create_default_https_context = ssl._create_unverified_context

authurl = "https://10.4.0.205/shterm/api/authenticate"
devurl = "https://10.4.0.205/shterm/api/dev"

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

def getDevinf(authtoken):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    dev_inf_url = devurl + '?nameNotLike=delete&sysType.id=2&size=1000'
    print(dev_inf_url)
    dev_inf_request = requests.get(dev_inf_url, headers=header, verify=False)
    return dev_inf_request.json()

def editDevinf(authtoken,devid,devname,devip,devtype,devowner,devsrv,devsrvport,devsrvproto,devsrvconsole):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    data = json.dumps\
        (
            {
                "name":devname+"@"+devip,
                "ip": devip,
                "sysType":{"id": devtype},
                "owner":{"id":devowner},
                "services":{"services":
                      {devsrv:
                           {"port":devsrvport ,
                            "proto": devsrvproto,
                            "rdp_console": devsrvconsole
                            }
                       }
                  }
             }
        )
    dev_inf_url = devurl+"/"+str(devid)
    print(dev_inf_url)
    dev_inf_request = requests.put(dev_inf_url, data, headers=header, verify=False)
    print(dev_inf_request.status_code)

if __name__ == "__main__":
    auth_token = getToken()
    dev_inf = getDevinf(auth_token)
    for s_dev_inf in dev_inf["content"]:
        dev_id = s_dev_inf["id"]
        dev_name = s_dev_inf["name"]
        dev_ip = s_dev_inf["ip"]
        dev_type = s_dev_inf["sysType"]["id"]
        dev_owner = s_dev_inf["owner"]["id"]
        for key,value in s_dev_inf["services"]["services"].items():
            dev_srv = key
            dev_srvport = value["port"]
            dev_srvproto = value["proto"]
            dev_srvconsole = value["rdp_console"]
            print(dev_id,dev_name,dev_ip,dev_type,dev_owner,dev_srv,dev_srvport,dev_srvproto,dev_srvconsole)
        editDevinf(auth_token,dev_id,dev_name,dev_ip,dev_type,dev_owner,dev_srv,dev_srvport,dev_srvproto,dev_srvconsole)
    getOff(auth_token)


