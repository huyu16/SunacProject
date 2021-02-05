#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzabbix import ZabbixAPI
import cx_Oracle
import os


os.environ["NLS_LANG"] = ".AL32UTF8"

zapi = ZabbixAPI('http://192.168.7.206/zabbix')
zapi.login('apiuser','pass@word1')
netdb = cx_Oracle.connect('app_mdesktop/Sunac@1918@10.3.0.179/middledb')
param_item = []
param_data = []
list_hisitem = []
list_curitem = []
list_hisdata = []

def get_setitem():
    #查询当前数据库中已有的itemid
    ItemCursor = netdb.cursor()
    sql = 'select itemid from mdesktop_dic'
    ItemHistory = ItemCursor.execute(sql)
    for s_itemhistory in ItemHistory:
        list_hisitem.append(s_itemhistory[0])
    #查询当前准备录入的itemid
    CurItem = zapi.item.get(filter={'name' : ['X1/0/24-内网防火墙上传流量','X2/0/24-内网防火墙上传流量']},
                            output=['itemid','name']
            )
    #判断itemid是否在数据库中，如果不存在添加到数据库中
    for s_setitem in CurItem[:]:
        if int(s_setitem['itemid']) in list_hisitem:
            CurItem.remove(s_setitem)
        else:
            pass
    ItemCursor.close()
    return CurItem

def process_dic_network():
    for s_item in get_setitem():
        #修改item为自定义命名
        if s_item['name'] == 'X1/0/24-内网防火墙上传流量':
            s_item['name'] = '内网防火墙上传流量'
        elif s_item['name'] == 'X2/0/24-内网防火墙上传流量':
            s_item['name'] = '内网防火墙上传流量'
        else:
            pass
        param_item.append((s_item["itemid"], s_item['name'], 'NETWORK'))
    return param_item

def get_setdata():
    TrendCursor1 = netdb.cursor()
    TrendCursor2 = netdb.cursor()
    sql1 = 'select itemid from mdesktop_dic'
    sql2 = 'select max(clock) from network_data'
    DataHistory1 = TrendCursor1.execute(sql1)
    DataHistory2 = TrendCursor2.execute(sql2)
    MaxData = DataHistory2.fetchone()
    #查询现有数据库中的clock时间最大值
    if MaxData is not None:
        #查询数据库中已有的数据字典itemid
        for s_hisdata in DataHistory1:
            list_hisdata.append(s_hisdata[0])
        #查询zabbix数据库中大于max(clock)的所有value
        SetTrend = zapi.trend.get(itemids=list_hisdata,
                                  time_from=MaxData[0],
                                  output=['itemid','clock','num','value_max']
               )
    else:
        #查询数据库中已有的数据字典itemid
        for s_hisdata in DataHistory1:
            list_hisdata.append(s_hisdata[0])
        #查询zabbix数据库中大于max(clock)的所有value
        SetTrend = zapi.trend.get(itemids=list_hisdata,
                                  output=['itemid','clock','num','value_max']
               )
    #删除max(clock)的值，因为time_from包含maxclock的值
    for s_settrend in SetTrend[:]:
        if int(s_settrend['clock']) == MaxData[0]:
            SetTrend.remove(s_settrend)
    print(SetTrend)
    TrendCursor1.close()
    TrendCursor2.close()
    return SetTrend

def process_data_network():
    for s_data in get_setdata():
        param_data.append((s_data['itemid'], s_data['clock'], s_data['num'], s_data['value_max']))
    return param_data

def insert_dic_network(v_dic):
    sql = "insert into mdesktop_dic(itemid, name, type) values(:1, :2, :3)"
    InsertDicCursor = netdb.cursor()
    try:
        InsertDicCursor.prepare(sql)  # 一次插入全部数据
        InsertDicCursor.executemany(None, v_dic)
        netdb.commit()
    except Exception as e:
        print(e)
        netdb.rollback()
    finally:
        InsertDicCursor.close()

def insert_data_network(v_data):
    sql = "insert into network_data(itemid, clock, num, value) values(:1, :2, :3, :4)"
    InsertDataCursor = netdb.cursor()
    try:
        InsertDataCursor.prepare(sql)  # 一次插入全部数据
        InsertDataCursor.executemany(None, v_data)
        netdb.commit()
    except Exception as e:
        print(e)
        netdb.rollback()
    finally:
        InsertDataCursor.close()

if __name__ == '__main__':
    #插入表network_dic数据
    inf_dic_network = process_dic_network()
    insert_dic_network(inf_dic_network)
    inf_data_network = process_data_network()
    insert_data_network(inf_data_network)

    netdb.close()
    zapi.user.logout()


