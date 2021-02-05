#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzabbix import ZabbixAPI

zabbixserver = 'http://10.4.0.107/zabbix'
zapi = ZabbixAPI(zabbixserver)
zapi.login("Admin","zabbix")

def get_hostsid():
    hostsid = zapi.host.get(output=['hostid','host'],
                            filter={'host':['printServer']},
                            selectInterfaces=['interfaceid','ip'],
                            )
    return hostsid

def get_itemsid(vhostid):
    itemsid = zapi.item.get(output=['itemid','name','interfaceid'],
                            hostids=vhostid,
                            search={'key_':'pyora'},
                            filter={'flags':0}
                            )
    return itemsid

def get_discoveryrules(vhostid):
    discoveryrulesid = zapi.discoveryrule.get(output=['itemid','name','interfaceid'],
                                            hostids=vhostid,
                                            search={'name':'Oracle'}
                                              )
    return discoveryrulesid

def get_itemprototypes(vhostid):
    itemprototypesid = zapi.itemprototype.get(output=['itemid','name','interfaceid'],
                                            hostids=vhostid,
                                            search={'name':'Oracle'}
                                                  )
    return itemprototypesid

def update_itemsid(vitemid,vinterfaceid):
    itemsid = zapi.item.update(itemid=vitemid,
                               interfaceid=vinterfaceid)
    return itemsid

def update_discoveryrulesid(vitemid,vinterfaceid):
    itemsid = zapi.discoveryrule.update(itemid=vitemid,
                               interfaceid=vinterfaceid)
    return itemsid

def update_itemprototypesid(vitemid,vinterfaceid):
    itemsid = zapi.itemprototype.update(itemid=vitemid,
                               interfaceid=vinterfaceid)
    return itemsid

if __name__ == '__main__':
    hostsid_list = get_hostsid()
    for p_host in hostsid_list:
        hostid = p_host['hostid']
        interfaceid_list = p_host['interfaces']
        for interface in interfaceid_list:
            if interface['ip'] == '10.4.0.119':
                interfaceid = interface['interfaceid']
                break

        itemsid_list = get_itemsid(hostid)
        discoveryrulesid_list = get_discoveryrules(hostid)
        itemprototypesid_list = get_itemprototypes(hostid)

        for itemid in itemsid_list:
            update_itemsid(itemid['itemid'],interfaceid)

        for discoveryruleid in discoveryrulesid_list:
            update_discoveryrulesid(discoveryruleid['itemid'],interfaceid)

        for itemprototypeid in itemprototypesid_list:
            update_itemprototypesid(itemprototypeid['itemid'],interfaceid)

        print(get_itemsid(hostid))
        print(get_discoveryrules(hostid))
        print(get_itemprototypes(hostid))






