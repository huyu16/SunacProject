#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import fileinput
import os
import re
import subprocess

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

hip=get_host_ip()
sip='10.4.0.106'

if os.path.isfile("/etc/zabbix/zabbix-agentd.conf"):
    for line in fileinput.input('/etc/zabbix/zabbix-agentd.conf',inplace=1):
        if re.search('Server=192.168.7.206',line):
            line='Server='+sip+'\n'
        elif re.search('ServerActive=192.168.7.206',line):
            line='ServerActive='+sip+'\n'
        elif re.search('Hostname=Agent',line):
            line='Hostname='+hip+'\n'
        elif re.search('HostMetadata=',line):
            line='HostMetadata=saphost\n'
        else:
            pass
        print(line),

else:
    pass

subprocess.call('chown root:zabbix /etc/zabbix/zabbix-agentd.conf',shell=True)
subprocess.call('service zabbix-agentd restart',shell=True)



