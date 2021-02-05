#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import AdOper
from ldap3 import Server, Connection, SUBTREE

# adconn = AdOper()

# server = Server('192.168.4.100')
# adconn = Connection(server, 'testing\\admin_adsrv', 'Sunac2020', auto_bind=True)

# adquery = adconn.adquery('ou=融创集团,dc=testing,dc=local',
#                          '(distinguishedName=OU=青岛文旅城(持有物业),OU=青岛公司,OU=北京区域集团,OU=融创集团,DC=testing,DC=local)')
# print(adquery)

a = ('1', '2', '3')

astr = str(a)
astr = astr.replace('1','2')
print(astr)

atup = tuple(astr)
print(atup)
