#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import argparse
    import pymssql
    import inspect
    import json

    class Checks(object):
        def check_db_count(self):
            """检查数据库数量"""
            sql = '''select count(1) from sys.databases '''
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def check_session_user(self):
            """检查数据库连通性"""
            sql = '''select count(1) from sys.dm_exec_sessions 
                    where program_name <> 'NULL' 
                    and program_name not like '%Agent%'
                    and program_name not like '%System%'
                    and login_name = 'sa' '''
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def check_active(self):
            """检查数据库连通性"""
            sql = "select 1+1"
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def check_database_status(self,dbname):
            """检查数据库状态"""
            sql = "select convert(nvarchar(50),(SELECT SERVERPROPERTY('productversion')))"
            self.cur.execute(sql)
            res = self.cur.fetchone()
            majorversion = int(res[0].split('.',1)[0])
            if majorversion < 11:
                sql1 = '''begin
                        SELECT db.name,CASE
                        WHEN db.state = 1 AND dbm.mirroring_state_desc = 'SYNCHRONIZED' THEN 21
                        WHEN db.state = 1 AND dbm.mirroring_state_desc = 'SYNCHRONIZING' THEN 22
                        WHEN db.state = 0 AND dbm.mirroring_state_desc = 'SYNCHRONIZED' THEN 23
                        WHEN db.state = 1 AND dbm.mirroring_state_desc IN ('DISCONNECTED','PENDING_FAILOVER','SUSPENDED','UNSYNCHRONIZED') THEN 25
                        WHEN db.state = 0 AND dbm.mirroring_state_desc IN ('DISCONNECTED','PENDING_FAILOVER','SUSPENDED','UNSYNCHRONIZED') THEN 26
                        WHEN db.state = 1 AND lsms.secondary_database = '{0}' THEN 41
                        ELSE db.state
                        END AS state
                        FROM sys.databases AS db LEFT JOIN master.sys.database_mirroring AS dbm ON db.database_id = dbm.database_id
                        LEFT JOIN msdb.dbo.log_shipping_monitor_secondary AS lsms ON db.name = lsms.secondary_database
                        WHERE db.name = '{0}'
                    end '''.format(dbname)
            else:
                 sql1 = '''begin
                        SELECT db.name,CASE
                        WHEN db.state = 1 AND dbm.mirroring_state_desc = 'SYNCHRONIZED' THEN 21
                        WHEN db.state = 1 AND dbm.mirroring_state_desc = 'SYNCHRONIZING' THEN 22
                        WHEN db.state = 0 AND dbm.mirroring_state_desc = 'SYNCHRONIZED' THEN 23
                        WHEN db.state = 1 AND dbm.mirroring_state_desc IN ('DISCONNECTED','PENDING_FAILOVER','SUSPENDED','UNSYNCHRONIZED') THEN 25
                        WHEN db.state = 0 AND dbm.mirroring_state_desc IN ('DISCONNECTED','PENDING_FAILOVER','SUSPENDED','UNSYNCHRONIZED') THEN 26
                        WHEN db.state = 0 AND hadr.synchronization_health = 2 THEN 31
                        WHEN db.state = 0 AND hadr.synchronization_health <> 2 THEN 35
                        WHEN db.state = 1 AND lsms.secondary_database = '{0}' THEN 41
                        ELSE db.state
                        END AS state
                        FROM sys.databases AS db LEFT JOIN master.sys.database_mirroring AS dbm ON db.database_id = dbm.database_id
                        LEFT JOIN (SELECT * FROM master.sys.dm_hadr_database_replica_states WHERE is_local = 1) AS hadr ON db.database_id = hadr.database_id
                        LEFT JOIN msdb.dbo.log_shipping_monitor_secondary AS lsms ON db.name = lsms.secondary_database
                        WHERE db.name = '{0}'
                    end '''.format(dbname)
            self.cur.execute(sql1)
            res = self.cur.fetchall()
            for i in res:
                print(i[1])

        def check_job_status(self,jobname):
            """检查数据库作业状态"""
            sql = '''IF EXISTS
                (SELECT TOP 1 JH.run_status 
                FROM msdb.dbo.sysjobhistory AS JH LEFT JOIN msdb.dbo.sysjobs AS J ON JH.job_id = J.job_id 
                WHERE J.name = '{0}' AND (JH.step_name in ('(Job outcome)','(作业结果)')))
                SELECT TOP 1 JH.run_status 
                FROM msdb.dbo.sysjobhistory AS JH LEFT JOIN msdb.dbo.sysjobs AS J ON JH.job_id = J.job_id 
                WHERE J.name = '{0}' AND (JH.step_name in ('(Job outcome)','(作业结果)'))
                ORDER BY JH.run_date DESC, JH.run_time DESC
                ELSE
                SELECT 11 AS 'run_status' '''.format(jobname)
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def check_backup_status(self,dbname):
            '''检查数据库备份状态'''
            sql = '''WITH LastBackUp AS
                (
                SELECT  bs.database_name,bs.backup_size,bs.backup_start_date,bmf.physical_device_name,Position = ROW_NUMBER() OVER( PARTITION BY bs.database_name ORDER BY bs.backup_start_date DESC )
                FROM  msdb.dbo.backupmediafamily bmf
                JOIN msdb.dbo.backupmediaset bms ON bmf.media_set_id = bms.media_set_id
                JOIN msdb.dbo.backupset bs ON bms.media_set_id = bs.media_set_id
                WHERE   bs.[type] in ('D','I','L')
                AND bs.is_copy_only = 0
                )
                SELECT sd.name AS [Database],
                case when DATEDIFF(dd,backup_start_date, getdate()) <= 2 then 0 
                else 1
                end  AS [msg],
                DATEDIFF (dd,backup_start_date, getdate()  ) AS [Days passed last backup]
                FROM (select * from sys.databases where name not in ('master','model','msdb','tempdb')) AS sd
                LEFT JOIN LastBackUp AS lb
                ON sd.name = lb.database_name AND Position = 1 
                where sd.name = '{0}'  '''.format(dbname)
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[1])

        def check_monitor_role(self, dbid):
            '''检查数据库镜像角色'''
            sql = "select a.mirroring_role from sys.database_mirroring a where database_id = '{0}' ".format(dbid)
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def check_alwayson_member_health(self):
            '''检查数据库Alwayson成员健康状态'''
            sql = '''SELECT COUNT (*) as NotHealtyCount FROM sys.dm_hadr_cluster_members
                    WHERE member_state_desc !='UP' '''
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def check_alwayson_member_role(self):
            '''检查数据库Alwayson成员角色'''
            sql = '''select AR.replica_server_name,HARS.group_id,HARS.role_desc,HARS.is_local
                    from sys.dm_hadr_availability_replica_states HARS
                    left join sys.availability_replicas AR on AR.group_id = HARS.group_id and AR.replica_id = HARS.replica_id 
                    where HARS.role_desc='PRIMARY' '''
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def check_alwayson_read_delay(self):
            '''检查数据库Alwayson读库延迟'''
            sql = '''select DATEDIFF(ss,last_commit_time,GETDATE()) 
                    from sys.dm_hadr_database_replica_states 
                    WHERE is_local = 0 '''
            self.cur.execute(sql)
            res = self.cur.fetchall()
            for i in res:
                print(i[0])

        def show_databases(self):
            """数据库JSON列表"""
            sql = "SELECT name FROM master..sysdatabases"
            self.cur.execute(sql)
            reslist = self.cur.fetchall()
            result_dict = {}
            data_list = []
            if reslist:
                for databasename in reslist:
                    result_dict = {"{#SQLINSTANCENAME}": self.instancename, "{#DBNAME}": databasename[0],
                                   "{#SQLINSTANCE}": self.sqlinstance}
                    data_list.append(result_dict)
            data_result = json.dumps({"data": data_list}, sort_keys=True, ensure_ascii=False, indent=4)
            print(data_result)

        def show_jobs(self):
            """数据库JSON列表"""
            sql = "SELECT name FROM msdb..sysjobs where enabled = 1"
            self.cur.execute(sql)
            reslist = self.cur.fetchall()
            result_dict = {}
            data_list = []
            if reslist:
                for jobname in reslist:
                    result_dict = {"{#SQLINSTANCENAME}": self.instancename, "{#JOBNAME}": jobname[0],
                                   "{#SQLINSTANCE}": self.sqlinstance}
                    data_list.append(result_dict)
            data_result = json.dumps({"data": data_list}, sort_keys=True, ensure_ascii=False, indent=4)
            print(data_result)

        def show_backup_database(self):
            """数据库JSON列表"""
            sql = "SELECT name FROM master..sysdatabases"
            self.cur.execute(sql)
            reslist = self.cur.fetchall()
            result_dict = {}
            data_list = []
            if reslist:
                for databasename in reslist:
                    result_dict = {"{#SQLINSTANCENAME}": self.instancename, "{#DBNAME}": databasename[0],
                                   "{#SQLINSTANCE}": self.sqlinstance}
                    data_list.append(result_dict)
            data_result = json.dumps({"data": data_list}, sort_keys=True, ensure_ascii=False, indent=4)
            print(data_result)

        def show_monitor_database(self):
            """镜像数据库列表"""
            sql = """select a.database_id dbid,b.name dbname from sys.database_mirroring a 
                     left join sys.databases b on a.database_id = b.database_id
                     where mirroring_guid is not null"""
            self.cur.execute(sql)
            reslist = self.cur.fetchall()
            result_dict = {}
            data_list = []
            if reslist:
                for databasename in reslist:
                    result_dict = {"{#SQLINSTANCENAME}": self.instancename, "{#DBID}": databasename[0],
                                   "{#DBNAME}": databasename[1],"{#SQLINSTANCE}": self.sqlinstance}
                    data_list.append(result_dict)
            data_result = json.dumps({"data": data_list}, sort_keys=True, ensure_ascii=False, indent=4)
            print(data_result)

    class Main(Checks):
        def __init__(self):
            parser = argparse.ArgumentParser()
            parser.add_argument('--sqlip')
            parser.add_argument('--instancename')
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
            self.instancename = a.instancename
            if self.instancename == 'MSSQLSERVER':
                fullInstancename = self.sqlipj
            else:
                fullInstancename = self.sqlip + '\\' + self.instancename
            if (self.instancename == 'MSSQLSERVER'):
                self.sqlinstance = "SQLServer"
            else:
                self.sqlinstance = 'MSSQL$' + self.instancename
            self.db = pymssql.connect(host=fullInstancename, database='master', user='zbmonitor', password='p1Zzw03d!_#8')
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
                print("error:"+str(err))

    if __name__ == "__main__":
        main = Main()
        main()
