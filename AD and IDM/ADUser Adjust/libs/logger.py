#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import re


def abs_filepath(childpath, filename):
    basepath = Path(Path(__file__).resolve().parent.parent)
    filepath = Path(basepath, childpath, filename)
    return filepath


def errlog_sys(syserrmsg):
    # 自定义logger
    syserrlogger = logging.getLogger("syserrlogger")
    # 自定义logger接收的日志级别
    syserrlogger.setLevel(logging.ERROR)
    # 判断列表是否已存在handle，如有不做创建
    if not syserrlogger.handlers:
        # 创建按日期分割的文件handle
        syserrhandle = TimedRotatingFileHandler(abs_filepath('logs', 'errorlog_sys'),
                                                when='midnight', encoding='utf-8', backupCount=7)
        syserrhandle.suffix = "%Y-%m-%d.log"
        syserrhandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 自定义日志格式
        syserrformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        # 将日志格式绑定handle
        syserrhandle.setFormatter(syserrformat)
        # 将handle绑定logger
        syserrlogger.addHandler(syserrhandle)
        # 输出信息
    else:
        pass
    syserrlogger.error(syserrmsg)


def debuglog_sys(sysdebugmsg):
    # 自定义logger
    sysdebuglogger = logging.getLogger("sysdebuglogger")
    # 自定义logger接收的日志级别
    sysdebuglogger.setLevel(logging.DEBUG)
    # 判断列表是否已存在handle，如有不做创建
    if not sysdebuglogger.handlers:
        # 创建按日期分割的文件handle
        sysdebughandle = TimedRotatingFileHandler(abs_filepath('logs', 'debuglog_sys'),
                                                  when='midnight', encoding='utf-8', backupCount=7)
        sysdebughandle.suffix = "%Y-%m-%d.log"
        sysdebughandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 自定义日志格式
        sysdebugformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        # 将日志格式绑定handle
        sysdebughandle.setFormatter(sysdebugformat)
        # 将handle绑定logger
        sysdebuglogger.addHandler(sysdebughandle)
        # 输出信息
    else:
        pass
    sysdebuglogger.error(sysdebugmsg)


def errlog_user(errmsg):
    # 自定义logger
    errlogger = logging.getLogger("errlogger")
    # 自定义logger接收的日志级别
    errlogger.setLevel(logging.ERROR)
    # 判断列表是否已存在handle，如有不做创建
    if not errlogger.handlers:
        # 创建按日期分割的文件handle
        errhandle = TimedRotatingFileHandler(abs_filepath('logs', 'errorlog_user'),
                                             when='midnight', encoding='utf-8', backupCount=7)
        errhandle.suffix = "%Y-%m-%d.log"
        errhandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 自定义日志格式
        errformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        # 将日志格式绑定handle
        errhandle.setFormatter(errformat)
        # 将handle绑定logger
        errlogger.addHandler(errhandle)
        # 输出信息
    else:
        pass
    errlogger.error(errmsg)


def infolog_user(infomsg):
    infologger = logging.getLogger("infologger")
    infologger.setLevel(logging.INFO)
    if not infologger.handlers:
        infohandle = TimedRotatingFileHandler(abs_filepath('logs', 'infolog_user'),
                                              when='midnight', encoding='utf-8', backupCount=7)
        infohandle.suffix = "%Y-%m-%d.log"
        infohandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        infoformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        infohandle.setFormatter(infoformat)
        infologger.addHandler(infohandle)
    else:
        pass
    infologger.info(infomsg)


def debuglog_user(debugmsg):
    # 自定义logger
    debuglogger = logging.getLogger("debuglogger")
    # 自定义logger接收的日志级别
    debuglogger.setLevel(logging.DEBUG)
    # 判断列表是否已存在handle，如有不做创建
    if not debuglogger.handlers:
        # 创建按日期分割的文件handle
        debughandle = TimedRotatingFileHandler(abs_filepath('logs', 'debuglog_user'),
                                               when='midnight', encoding='utf-8', backupCount=7)
        debughandle.suffix = "%Y-%m-%d.log"
        debughandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 自定义日志格式
        debugformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        # 将日志格式绑定handle
        debughandle.setFormatter(debugformat)
        # 将handle绑定logger
        debuglogger.addHandler(debughandle)
        # 输出信息
    else:
        pass
    debuglogger.debug(debugmsg)


def errlog_org(orgerrmsg):
    # 自定义logger
    orgerrlogger = logging.getLogger("org_errlogger")
    # 自定义logger接收的日志级别
    orgerrlogger.setLevel(logging.ERROR)
    # 判断列表是否已存在handle，如有不做创建
    if not orgerrlogger.handlers:
        # 创建按日期分割的文件handle
        orgerrhandle = TimedRotatingFileHandler(abs_filepath('logs', 'errorlog_org'),
                                                when='midnight', encoding='utf-8', backupCount=7)
        orgerrhandle.suffix = "%Y-%m-%d.log"
        orgerrhandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 自定义日志格式
        orgerrformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        # 将日志格式绑定handle
        orgerrhandle.setFormatter(orgerrformat)
        # 将handle绑定logger
        orgerrlogger.addHandler(orgerrhandle)
        # 输出信息
    else:
        pass
    orgerrlogger.error(orgerrmsg)


def infolog_org(orginfomsg):
    orginfologger = logging.getLogger("org_infologger")
    orginfologger.setLevel(logging.INFO)
    if not orginfologger.handlers:
        orginfohandle = TimedRotatingFileHandler(abs_filepath('logs', 'infolog_org'),
                                                 when='midnight', encoding='utf-8', backupCount=7)
        orginfohandle.suffix = "%Y-%m-%d.log"
        orginfohandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        orginfoformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        orginfohandle.setFormatter(orginfoformat)
        orginfologger.addHandler(orginfohandle)
    else:
        pass
    orginfologger.info(orginfomsg)


def debuglog_org(orgdebugmsg):
    # 自定义logger
    orgdebuglogger = logging.getLogger("org_debuglogger")
    # 自定义logger接收的日志级别
    orgdebuglogger.setLevel(logging.DEBUG)
    # 判断列表是否已存在handle，如有不做创建
    if not orgdebuglogger.handlers:
        # 创建按日期分割的文件handle
        orgdebughandle = TimedRotatingFileHandler(abs_filepath('logs', 'debuglog_org'),
                                                  when='midnight', encoding='utf-8', backupCount=7)
        orgdebughandle.suffix = "%Y-%m-%d.log"
        orgdebughandle.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 自定义日志格式
        orgdebugformat = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        # 将日志格式绑定handle
        orgdebughandle.setFormatter(orgdebugformat)
        # 将handle绑定logger
        orgdebuglogger.addHandler(orgdebughandle)
        # 输出信息
    else:
        pass
    orgdebuglogger.debug(orgdebugmsg)
