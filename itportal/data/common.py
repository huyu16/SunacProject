#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql


class MysqlOper:
    def __init__(self):
        self.host = '10.4.64.2'
        self.user = 'itportal'
        self.passwd = 'P@ssw0rd'
        self.dbname = 'itportal'
        self.charset = 'utf8'
        self.dbconn = self.dbconnect()

        if self.dbconn:
            self.dbcursor = self.dbconn.cursor()

    def dbconnect(self):
        mysqlconn = ''
        mysqlconn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    passwd=self.passwd,
                                    db=self.dbname,
                                    charset=self.charset)
        return mysqlconn

    def dbclose(self):
        if self.dbconn:
            if self.dbcursor:
                self.dbcursor.close()
            if self.dbconn:
                self.dbconn.close()

    def dbmanyquery(self, sql, *args):
        """
        执行多行查询语句
        """
        resmany = ''
        if self.dbconn:
            self.dbcursor.execute(sql, args)
            resmany = self.dbcursor.fetchall()
        return resmany

    def dbonequery(self, sql, *args):
        resone = ''
        if self.dbconn:
            self.dbcursor.execute(sql, args)
            resone = self.dbcursor.fetchone()
        return resone

    def dbmanyinsert(self, sql, l_value):
        if self.dbconn:
            try:
                self.dbcursor.executemany(sql, l_value)
                self.dbconn.commit()
                return 1
            except Exception as e:
                self.dbconn.rollback()
                return 0

    def dbonemod(self, sql, *args):
        if self.dbconn:
            try:
                self.dbcursor.execute(sql, args)
                self.dbconn.commit()
                return 1
            except Exception as e:
                self.dbconn.rollback()
                return 0
