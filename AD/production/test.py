#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ldap3 import Server, Connection, SUBTREE

HOSTBJJNOU = 'OU=BJ_JN_COMP,OU=BJ_COMPUTER,OU=北京区域集团,OU=融创集团,DC=SUNAC,DC=local'
HOSTBJTYOU = 'OU=BJ_TY_COMP,OU=BJ_COMPUTER,OU=北京区域集团,OU=融创集团,DC=SUNAC,DC=local'
HOSTBJOTHEROU = 'OU=BJ_OTHER_COMP,OU=BJ_COMPUTER,OU=北京区域集团,OU=融创集团,DC=SUNAC,DC=local'

server = Server('192.168.4.200')
adconn = Connection(server, 'sunac\\jt_srv_ad', 'pass@word1', auto_bind=True)

ADN = 'DC=SUNAC,DC=local'
BDN = 'OU=融创集团,DC=SUNAC,DC=local'

adquery = adconn.search(search_base=BDN,
                        search_filter="(&(objectClass=computer)(name=BJ-*)(!(OU=BJ_OTHER_COMP)))",
                        attributes=['name'],
                        # search_filter='(objectClass=person)',
                        search_scope='SUBTREE'
                        )

for aduserobj in adconn.response:
    hostname = aduserobj['attributes']['name']
    str_hostolddn = aduserobj['dn']
    l_hostolddn = str_hostolddn.split(',')
    hostcn = l_hostolddn[0]
    # print(hostcn)
    l_hostoldou = l_hostolddn[1:]
    hostoldou = ','.join(l_hostoldou)
    # print(hostoldou)
    #
    # if hostname.startswith('BJ-JN-'):
    #     print('BJ-JN')
    #     if hostoldou != HOSTBJJNOU:
    #         res_bjjn = adconn.modify_dn(str_hostolddn, hostcn, new_superior=HOSTBJJNOU)
    #         print(res_bjjn)
    # elif hostname.startswith('BJ-TY-'):
    #     print('BJ-TY')
    #     if hostoldou != HOSTBJTYOU:
    #         res_bjty = adconn.modify_dn(str_hostolddn, hostcn, new_superior=HOSTBJTYOU)
    #         print(res_bjty)
    # elif hostname.startswith('BJ-'):
    #     print('BJ')
    #     if hostoldou != HOSTBJOTHEROU:
    #         res_bjother = adconn.modify_dn(str_hostolddn, hostcn, new_superior=HOSTBJOTHEROU)
    #         print(res_bjother)

adconn.unbind()



