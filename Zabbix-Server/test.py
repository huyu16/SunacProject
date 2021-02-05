#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,json,os
from datetime import datetime,timedelta

urlevent = "http://10.4.64.3:9000/api/events/search"
init_list = [{'messageid':"ABCD",'messagetime':'2020-07-21T10:14:47.933Z'}]
file_path = 'C://QLDownload//test_file.json'
list_messageid = []

header = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Requested-By": "cli"
}

data = {
    "timerange": {
        "type": "relative",
        "range": 86400
        },
    "filter": {
        "event_definitions": ["网络-华为三层事件(微信)"]
        }
    }

if os.path.exists(r'C:\QLDownload\test_file.json'):
    pass
else:
    f = open(r'C:\QLDownload\test_file.json', 'w',encoding='utf8')
    jsondata = json.dumps(init_list, indent=4, separators=(',', ': '))
    f.write(jsondata)
    f.close()

file = open(file_path, 'r')
list_file_data = json.load(file)
for s_messageid in list_file_data:
    list_messageid.append(s_messageid["messageid"])
file.close()

s = requests.Session()
s.auth = ('huy33', '123456')
set_event = s.post(url = urlevent, headers = header, data = json.dumps(data))
dic_event = set_event.json()

if dic_event['events']:
    # print(list_messageid)
    for event in dic_event['events']:
        if event['event']['id'] not in list_messageid:
            # print(event['event']['origin_context'].split(":"))
            e_index = event['event']['origin_context'].split(":")[4]
            e_messagecode = event['event']['origin_context'].split(":")[5]
            # print(e_index,e_messageid)
            set_message = s.get(url="http://10.4.64.3:9000/api/messages/" + e_index + "/" + e_messagecode)
            dic_message = set_message.json()
            m_devname = dic_message["message"]["fields"]["DeviceName"]
            m_devip = dic_message["message"]["fields"]["gl2_remote_ip"]
            m_sourceip = dic_message["message"]["fields"]["sourceip"]
            m_utctime = dic_message["message"]["fields"]["timestamp"]
            m_time = datetime.strptime(m_utctime.split('.')[0], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)
            altercontext = "被攻击设备名：" + m_devname + " 被攻击IP：" + m_devip + " 攻击源IP：" + m_sourceip + " 攻击时间：" + m_time.strftime("%Y-%m-%d %H:%M:%S")
            cmdcontext = '/usr/bin/zabbix_sender -s "dcxservagg" -z 10.4.0.106 -k "huaweinetworklog" -o "' + altercontext + '"'
            print(cmdcontext)
            # os.system(cmdcontext)
            #list_file_data.append({"messageid":event['event']['id'],"messagetime":event["event"]["timestamp"]})
            #print(list_file_data)
else:
    print('nodata')
    # os.system('/usr/bin/zabbix_sender -s "dcxservagg" -z 10.4.0.106 -k "huaweinetworklog" -o "nodata" ')


# f_dump = open(file_path, 'w', encoding='utf8')
# json.dump(list_file_data, f_dump, indent=4, separators=(',', ': '))
# f.close()

print(type(list_file_data))
print('123')

