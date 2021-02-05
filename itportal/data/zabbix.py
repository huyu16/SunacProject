#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzabbix import ZabbixAPI

zapi = ZabbixAPI('http://10.4.0.107/zabbix')
zapi.login("Admin", "pass@word1")


def get_zhosts():
    api_zhostslist = zapi.host.get(output=['name'],
                                   filter={'status': 0},
                                   search={'name': 'ESXI'},
                                   excludeSearch='true',
                                   selectInterfaces=['interfaceid', 'ip', 'main'])
    return api_zhostslist


if __name__ == "__main__":
    zhostsset = get_zhosts()
    zhostlist = []
    for zhostinf in zhostsset:
        for zhost_interface in zhostinf['interfaces']:
            if zhost_interface.get('main') == '1':
                zhostlist.append(zhost_interface['ip'])
    print(zhostlist)
