#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, ssl

ssl._create_default_https_context = ssl._create_unverified_context

authurl = "https://10.4.0.205/shterm/api/authenticate"
userurl = "https://10.4.0.205/shterm/api/user"


def getToken():
    header = {'Content-type': 'application/json; charset=utf-8'}
    data = json.dumps({'username': 'admin', 'password': 'RIS@sunac2019'})
    auth = requests.post(authurl, data, headers=header, verify=False)
    return auth.json()['ST_AUTH_TOKEN']


def getOff(authtoken):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    httpcode = requests.delete(authurl, headers=header, verify=False)
    if httpcode.status_code == 204:
        print('注销成功')
    else:
        print('注销失败')


def getUserinf(authtoken):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    user_inf_url = userurl + '?role.id=5&extInfo.36=供方'
    print(user_inf_url)
    user_inf_request = requests.get(user_inf_url, headers=header, verify=False)
    return user_inf_request.json()


def editUserinf(authtoken, userid, username, userauthtype, userdep):
    header = \
        {
            'Content-type': 'application/json; charset=utf-8',
            "st-auth-token": authtoken
        }
    data = json.dumps \
            (
            {
                "userName": username,
                "role": {"id": 102},
                "authType": {"id": userauthtype},
                "department": {"id": userdep}
            }
        )
    user_inf_url = userurl + "/" + str(userid)
    print(user_inf_url)
    user_inf_request = requests.put(user_inf_url, data, headers=header, verify=False)
    print(user_inf_request.status_code)


if __name__ == "__main__":
    auth_token = getToken()
    user_inf = getUserinf(auth_token)
    print(user_inf)
    for s_user_inf in user_inf["content"]:
        user_id = s_user_inf["id"]
        user_name = s_user_inf["userName"]
        user_authtype = s_user_inf["authType"]["id"]
        user_dep = s_user_inf["department"]["id"]
        print(auth_token, user_id, user_name, user_authtype, user_dep)
        editUserinf(auth_token, user_id, user_name, user_authtype, user_dep)
    getOff(auth_token)
