#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzabbix import ZabbixAPI

zabbixserver = 'http://10.4.0.107/zabbix'
zapi = ZabbixAPI(zabbixserver)
zapi.login("Admin","zabbix")

items = zapi.item.get(output=['itemid','name','interfaceid'],
                        search={'key_':'pyora'},
                        filter={'flags':0}
                        )

print(items)


