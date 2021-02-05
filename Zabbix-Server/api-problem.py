#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pyzabbix import ZabbixAPI

dt = "2020-3-15 00:00:00"
timearray = time.strptime(dt,"%Y-%m-%d %H:%M:%S")
timestamp = time.mktime(timearray)

zabbixserver = 'http://10.4.0.107/zabbix'
zapi = ZabbixAPI(zabbixserver)
zapi.login("Admin","pass@word1")

list_problem = zapi.problem.get(time_from=timestamp)
print(list_problem)


#1558019052

#1572793868