#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import urllib3
from data import ris
# from overview.models import UserExpire

l_risuser = []

auth_token = ris.gettoken()
userinf = ris.get_extuser(auth_token)

# for id_extuser in l_extuser:

ris.getoff(auth_token)

for obj_userinf in userinf['content']:
    l_risuser.append(obj_userinf['loginName'])
print(l_risuser)

# res_tempuser = list(UserExpire.objects.filter(userid__in=l_risuser).values
#                     ('userid', 'username', 'company', 'phone', 'email',
#                      'state', 'expiretime', 'manager')
#                     )
#
# print(res_tempuser)