#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pymysql
import inspect
import json

class Checks(object):
    def check_active(self):
        """检查数据库连通性"""
        sql = "select 1+1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def check_database_status(self,mysql_status):
        """检查数据库状态"""
        sql = "show global status where variable_name = '{0}' " .format(mysql_status)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[1])

    def check_database_variables(self,mysql_variable):
        """检查数据库配置"""
        sql = "show global variables where variable_name = '{0}' " .format(mysql_variable)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            if i[1] == 'ON' or i[1] == 'YES':
                print(1)
            elif i[1] == 'OFF' or i[1] == 'NO':
                print(0)
            else:
                print(i[1])

    def check_replication_status(self):
        '''检查读库复制状态'''
        sql = "show slave status"
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res == None:
            print(2)
        else:
            collist = []
            for i in self.cur.description:
                collist.append(i[0])
            datadic = dict(zip(collist, res))
            if datadic["Slave_IO_Running"] == 'Yes' and datadic['Slave_SQL_Running'] == 'Yes':
                print(0)
            else:
                print(1)

    def check_backup_status(self):
        '''检查主库备份状态'''
        sql1 = '''select status from cf_backup_info.cf_backup_info
                  WHERE backup_date > DATE_SUB( sysdate( ), INTERVAL 1 DAY )'''
        self.cur.execute(sql1)
        res = self.cur.fetchall()
        if res:
            n = 0
            for i in res:
                if i[0] == 'FAILED':
                    n = n + 1
            print(n)
        else:
            print(99)

    def check_processlist_count(self):
        '''检查数据库进程数量'''
        sql = "select count(*) from information_schema.processlist "
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

    def check_processlist_waiting(self):
        '''检查数据库进程数量'''
        sql = '''select count(*) from information_schema.processlist 
                where state like '%Waiting%' '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i[0])

class Main(Checks):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--sqlip')
        parser.add_argument('--port')
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
        self.sqlip = a.sqlip
        self.port = int(a.port)
        self.db = pymysql.connect(host=self.sqlip, port=self.port, user='zbmonitor', password='p1Zzw03d!_#8')
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
            print("error:" + str(err))

if __name__ == "__main__":
    main = Main()
    main()
