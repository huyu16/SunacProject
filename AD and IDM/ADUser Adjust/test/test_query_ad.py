#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import AdOper
from ldap3 import Server, Connection, SUBTREE

adconn = AdOper()

# server = Server('192.168.4.100')
# adconn = Connection(server, 'testing\\admin_adsrv', 'Sunac2020', auto_bind=True)
test = 'anfl'
adfilterstr = f'(&(objectClass=person)(sAMAccountName={test.lower()})(!(userAccountControl=514)))'
adquery = adconn.adquery('ou=融创集团,dc=testing,dc=local', adfilterstr)
print(adquery)
print(adconn.adconn.response)

if adquery:
    print('YES')
else:
    print('NO')

