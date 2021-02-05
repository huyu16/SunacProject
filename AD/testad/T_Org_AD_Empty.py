#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testad.logger import infolog_org, errlog_org
from ldap3 import Server, Connection

server = Server('192.168.4.200')
adconnou = Connection(server, 'sunac\\jt_srv_ad', 'pass@word1', auto_bind=True)
adconnuser = Connection(server, 'sunac\\jt_srv_ad', 'pass@word1', auto_bind=True)

adconnou.search(search_base='ou=北京区域集团,ou=融创集团,dc=SUNAC,dc=local',
                search_filter='(objectClass=organizationalUnit)')

for obj_adou in adconnou.response:
    adou = obj_adou['dn']
    adconnuser.search(search_base=adou,
                      search_filter='(objectClass=person)')
    l_aduser = []
    for obj_aduser in adconnuser.response:
        l_aduser.append(obj_aduser['dn'])
    if len(l_aduser) == 0:
        print(adou)
