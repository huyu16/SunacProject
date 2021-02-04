#!/usr/bin/env python3
# coding: utf-8

import argparse
import cx_Oracle
import inspect
import json
import re

class Checks(object):
    def check_backup(self):
        """Check Intance is active and open"""
        res = 0
        sql = '''select status
                  FROM  v$rman_backup_job_details
                  WHERE  start_time > SYSDATE - 1
                  ORDER  BY END_TIME '''
        self.cur.execute(sql)
        curres = self.cur.fetchall()
        rescount = (self.cur.rowcount)
        if rescount == 0:
            res = 99
            print(res)
        else:
            for i in curres:
                if re.search('FAILED|ERROR', i[0]):
                    res = res + 1
            print(res)

    def check_dg(self):
        """Check Intance is active and open"""
        sql = '''select sum(applied) applied from 
                (select case when applied = 'YES' then 1 else 0 end as applied 
                from (select row_number() over(order by a.FIRST_TIME desc) rd,
                sequence#,standby_dest,archived,applied 
                from v$archived_log a where a.standby_dest = 'YES') 
                where rd < 5) '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def check_active(self):
        """Check Intance is active and open"""
        sql = '''select to_char(case when inst_cnt > 0 then 1 else 0 end, 
              'FM99999999999999990') retvalue from (select count(*) inst_cnt 
              from v$instance where status = 'OPEN' and logins = 'ALLOWED' 
              and database_status = 'ACTIVE')'''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def rcachehit(self):
        """Read Cache hit ratio"""
        sql = '''SELECT to_char((1 - (phy.value - lob.value - dir.value) / 
              ses.value) * 100, 'FM99999990.9999') retvalue 
              FROM   v$sysstat ses, v$sysstat lob, 
              v$sysstat dir, v$sysstat phy 
              WHERE  ses.name = 'session logical reads' 
              AND    dir.name = 'physical reads direct' 
              AND    lob.name = 'physical reads direct (lob)' 
              AND    phy.name = 'physical reads' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def query_sysmetrics(self, name):
        """Query v$sysmetric parameters"""
        sql = '''select value from v$sysmetric 
                where METRIC_NAME ='{0}' and rownum <=1 
                order by INTSIZE_CSEC '''.format(name.replace('_', ' '))
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def activeusercount(self):
        """Count of active users"""
        sql = '''select to_char(count(*)-1, 'FM99999999999999990') retvalue 
              from v$session where username is not null 
              and status='ACTIVE' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def version(self):
        """Oracle version (Banner)"""
        sql = "select banner from v$version where rownum=1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def uptime(self):
        """Instance Uptime (seconds)"""
        sql = '''select to_char((sysdate-startup_time)*86400, 
              'FM99999999999999990') retvalue from v$instance '''
        self.cur.execute(sql)
        res = self.cur.fetchmany(numRows=3)
        for i in res:
            print(i[0])

    def commits(self):
        """User Commits"""
        sql = '''select to_char(value, 'FM99999999999999990') retvalue from 
              v$sysstat where name = 'user commits' '''
        self.cur.execute(sql)
        res = self.cur.fetchmany(numRows=3)
        for i in res:
            print(i[0])

    def deadlocks(self):
        """Deadlocks"""
        sql = '''select to_char(value, 'FM99999999999999990') retvalue from 
              v$sysstat where name = 'enqueue deadlocks' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def tblscans(self):
        """Table scans (long tables)"""
        sql = '''select to_char(value, 'FM99999999999999990') retvalue from 
              v$sysstat where name = 'table scans (long tables)' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def tblrowsscans(self):
        """Table scan rows gotten"""
        sql = '''select to_char(value, 'FM99999999999999990') retvalue from 
              v$sysstat where name = 'table scan rows gotten' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def indexffs(self):
        """Index fast full scans (full)"""
        sql = '''select to_char(value, 'FM99999999999999990') retvalue from 
              v$sysstat where name = 'index fast full scans (full)' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def bufbusywaits(self):
        """Buffer busy waits"""
        sql = '''select to_char(time_waited, 'FM99999999999999990') retvalue 
              from v$system_event se, v$event_name en 
              where se.event(+) = en.name and en.name = 'buffer busy waits' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def logswcompletion(self):
        """log files switch completion"""
        sql = '''select to_char(time_waited, 'FM99999999999999990') retvalue 
              from v$system_event se, v$event_name en where se.event(+) 
              = en.name and en.name = 'log files switch completion' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def logfilesync(self):
        """Log files sync"""
        sql = '''select to_char(time_waited, 'FM99999999999999990') retvalue 
              from v$system_event se, v$event_name en 
              where se.event(+) = en.name and en.name = 'log files sync' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def logprllwrite(self):
        """Log files parallel write"""
        sql = '''select to_char(time_waited, 'FM99999999999999990') retvalue 
              from v$system_event se, v$event_name en where se.event(+) 
              = en.name and en.name = 'log files parallel write' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def tablespace(self, name):
        """Get tablespace usage"""
        sql = '''SELECT tablespace_name "TABLESPACE", used_percent "USED" 
                FROM  dba_tablespace_usage_metrics 
                WHERE tablespace_name = '{0}' '''.format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[1])

    def tablespace_abs(self, name):
        """Get tablespace in free"""
        sql = '''SELECT tablespace_name "TABLESPACE", 
                round((tablespace_size - used_space) * 8192, 2) "BYTES" 
                FROM dba_tablespace_usage_metrics 
                WHERE  tablespace_name = '{0}' '''.format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[1])

    def tablespace_slave(self, name):
        """Get tablespace usage"""
        sql = '''SELECT D.TABLESPACE_NAME TABLESPACE, 
              ROUND(((SPACE - NVL(FREE_SPACE, 0)) / MAX_SPACE) * 100, 2) USED 
              FROM (SELECT TABLESPACE_NAME,SUM(MAX_SPACE) MAX_SPACE,SUM(SPACE) SPACE,SUM(BLOCKS) BLOCKS 
              FROM (SELECT TABLESPACE_NAME, 
              ROUND(decode(AUTOEXTENSIBLE,'YES',SUM(MAXBYTES) / (1024 * 1024),SUM(BYTES) 
              / (1024 * 1024)),2) MAX_SPACE, 
              ROUND(SUM(BYTES) / (1024 * 1024), 2) SPACE,SUM(BLOCKS) BLOCKS FROM DBA_DATA_FILES 
              GROUP BY TABLESPACE_NAME, AUTOEXTENSIBLE) 
              GROUP BY TABLESPACE_NAME) D, 
              (SELECT TABLESPACE_NAME, 
              ROUND(SUM(BYTES) / (1024 * 1024), 2) FREE_SPACE 
              FROM DBA_FREE_SPACE GROUP BY TABLESPACE_NAME) F, 
              dba_tablespaces G 
              WHERE D.TABLESPACE_NAME = F.TABLESPACE_NAME(+) AND D.TABLESPACE_NAME = G.TABLESPACE_NAME 
              AND D.TABLESPACE_NAME='{0}' '''.format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[1])

    def asm_volume_puse(self, name):
        """Get ASM volume usage"""
        sql = '''select round(((TOTAL_MB-FREE_MB)/TOTAL_MB*100),2) 
              from v$asm_diskgroup_stat where name = '{0}' '''.format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def asm_volume_free(self, name):
        sql = "select FREE_MB*1024*1024 from v$asm_diskgroup_stat where name = '{0}' ".format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def query_lock(self):
        """Query lock"""
        sql = "SELECT count(*) FROM gv$lock l WHERE  block=1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def query_sessions(self):
        """Query Sessions"""
        sql = '''select count(*) from gv$session 
                where username is not null and status='ACTIVE' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def show_tablespaces(self):
        """List tablespace names in a JSON like format for Zabbix use"""
        sql = "SELECT TABLESPACE_NAME FROM DBA_TABLESPACES WHERE CONTENTS <> 'TEMPORARY' ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['{#TABLESPACE}']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        print(json.dumps({'data': lst}))

    def show_asm_volumes(self):
        """List als ASM volumes in a JSON like format for Zabbix use"""
        sql = "select NAME from v$asm_diskgroup_stat ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['{#ASMVOLUME}']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        print(json.dumps({'data': lst}))

class Main(Checks):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--sqlip')
        parser.add_argument('--sqlport')
        parser.add_argument('--sqlinstance')

        subparsers = parser.add_subparsers()

        for name in dir(self):
            if not name.startswith("_"):
                p = subparsers.add_parser(name)
                method = getattr(self, name)
                argnames = inspect.getfullargspec(method).args[1:]
                for argname in argnames:
                    p.add_argument(argname)
                p.set_defaults(func=method, argnames=argnames)
        self.args = parser.parse_args()

    def db_connect(self):
        a = self.args
        sqlip = a.sqlip
        sqlport = int(a.sqlport)
        sqlinstance = a.sqlinstance
        self.db = cx_Oracle.connect("zbmonitor/p1Zzw03d!_#8@{0}:{1}/{2}".format(sqlip, sqlport, sqlinstance))
        self.cur = self.db.cursor()

    def db_close(self):
        self.db.close()

    def __call__(self):
        try:
            a = self.args
            callargs = [getattr(a, name) for name in a.argnames]
            self.db_connect()
            try:
                return self.args.func(*callargs)
            finally:
                self.db_close()
        except Exception as err:
            print(0)
            print(str(err))

if __name__ == "__main__":
    main = Main()
    main()
