#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ldap3 import Server, Connection, SUBTREE, LEVEL, BASE
import pymysql
from testad.t_logger import infolog_comp, errlog_comp
import re


def comparea(v_areaid):
    server = Server('192.168.4.100')
    adconn = Connection(server, 'testing\\admin_adsrv', 'Sunac2020', auto_bind=True)

    dbconn = pymysql.connect(
        host='10.4.64.2',
        user='aduser',
        passwd='ADuser@123',
        db='test_ad',
        charset='utf8')
    dbcursor = dbconn.cursor()

    dbcursor.execute('select compprefix, areadn from sum_inf_area '
                     'where parentid = %s order by compprefix desc' % v_areaid)
    t_adcomp = dbcursor.fetchall()

    dbcursor.execute('select compprefix, areadn from sum_inf_area where areaid = %s' % v_areaid)
    areaou = dbcursor.fetchone()

    adconn.search(search_base='OU=融创集团,DC=testing,DC=local',
                  search_filter=f"(&(objectClass=computer)(name={areaou[0]}*))",
                  attributes=["name"]
                  )
    for obj_adcomp in adconn.response:
        hostname = obj_adcomp['attributes']['name']
        str_hostolddn = obj_adcomp['dn']
        hostolddn = str_hostolddn.split(',')
        hostcn = hostolddn[0]
        l_hostoldou = hostolddn[1:]
        hostoldou = ','.join(l_hostoldou)
        if re.search(f'OU={areaou[0]}_COMP_', hostoldou):
            pass
        else:
            for adcomp in t_adcomp:
                if hostname.startswith(adcomp[0]):
                    if hostoldou != adcomp[1]:
                        res_compou = adconn.modify_dn(str_hostolddn, hostcn, new_superior=adcomp[1])
                        if res_compou:
                            infolog_comp(f"AD信息--移动计算机帐号成功 {hostname} 从 {hostoldou} 到 {adcomp[1]}")
                        else:
                            errlog_comp(f"AD信息--移动计算机帐号失败 {hostname} 从 {hostoldou} 到 {adcomp[1]}")
                        break
                    else:
                        break

    adconn.unbind()
    dbcursor.close()
    dbconn.close()


if __name__ == "__main__":
    comparea('000104')
