#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import urllib3
from data import ris

auth_token = ris.gettoken()

extuserinf = ris.get_extuser(auth_token)

l_extuser = []

print(extuserinf)

for obj_extuser in extuserinf['content']:
    l_extuser.append(obj_extuser['loginName'])

# for id_extuser in l_extuser:

ris.getoff(auth_token)

