#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler


def errlog_user(errmsg):
    # 自定义logger
    errlogger = logging.getLogger("errlogger")
    # 自定义logger接收的日志级别
    errlogger.setLevel(logging.ERROR)
    # 判断列表是否已存在handle，如有不做创建
    if not errlogger.handlers:
        # 创建按日期分割的文件handle
        errhandle = TimedRotatingFileHandler('errorlog_user', when='midnight', encoding='utf-8')
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
        infohandle = TimedRotatingFileHandler('infolog_user', when='midnight', encoding='utf-8')
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
        debughandle = TimedRotatingFileHandler('debuglog_user', when='midnight', encoding='utf-8')
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
        orgerrhandle = TimedRotatingFileHandler('errorlog_org', when='midnight', encoding='utf-8')
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
        orginfohandle = TimedRotatingFileHandler('infolog_org', when='midnight', encoding='utf-8')
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
        orgdebughandle = TimedRotatingFileHandler('debuglog_org', when='midnight', encoding='utf-8')
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
