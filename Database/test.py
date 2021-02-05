#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cx_Oracle

f = open(r"C:\Users\zxcvb\Documents\CloudStation\dberr.log",'a',encoding='utf-8')
try:
    db = cx_Oracle.connect("zbmonitor/p1Zzw03d!_#8@192.168.2.113/rcdw")
    cur = db.cursor()
    try:
        sql = '''select to_char(case when inst_cnt > 0 then 1 else 0 end, 
                      'FM99999999999999990') retvalue from (select count(*) inst_cnt 
                      from v$instance where status = 'OPEN' and logins = 'ALLOWED' 
                      and database_status = 'ACTIVE') '''
        cur.execute(sql)
        res = cur.fetchall()
        for i in res:
            print(i[0])
    except Exception as err1:
        f.write(str(err1))
    finally:
        db.close()
except Exception as err:
    f.write(str(err)+'\n')
finally:
    f.close()


