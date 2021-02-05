#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzabbix import ZabbixAPI

zabbixserver = 'http://10.4.0.107/zabbix'
zapi = ZabbixAPI(zabbixserver)
zapi.login("Admin","pass@word1")

def get_templatesid():
    templatesid = zapi.template.get(output=['templateid','host'],
                                    filter={'host':['Template DB Sqlserver Database 1']},
                                    )
    return templatesid

def get_hostsid(vtemplateid):
    hostsid = zapi.host.get(output=['hostid','host','name'],
                            templateids=[vtemplateid],
                            selectInterfaces=['interfaceid','ip'],
                            )
    return hostsid

def get_itemsid(vhostid):
    itemsid = zapi.item.get(output=['itemid','name','interfaceid'],
                            hostids=vhostid,
                            filter={'flags':0,'name':'SQL Instance {$SQLINSTANCENAME1}: Check Database Count'}
                            )
    return itemsid

def update_itemsid(vitemid,vinterfaceid):
    itemsid = zapi.item.update(itemid=vitemid,
                               interfaceid=vinterfaceid)
    return itemsid

if __name__ == '__main__':
    templatesid_list = get_templatesid()
    for templateid in templatesid_list:
        hostsid_list = get_hostsid(templateid['templateid'])
        for p_host in hostsid_list:
            hostid = p_host['hostid']
            interfaceid_list = p_host['interfaces']
            for interface in interfaceid_list:
                if interface['ip'] == '10.4.0.119':
                    interfaceid = interface['interfaceid']
                    break

            itemsid_list = get_itemsid(hostid)
            print(itemsid_list)

            for itemid in itemsid_list:
                update_itemsid(itemid['itemid'], interfaceid)
                print(get_itemsid(hostid))




