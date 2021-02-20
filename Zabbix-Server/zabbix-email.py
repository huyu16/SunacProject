#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from smtplib import SMTP

HOST = "mail.sunac.com.cn"  # 定义smtp主机
SUBJECT = "test email form python"  # 定义邮件主题
TO = "andyzhao99@126.com"  # 定义邮件收件人
FROM = "liuzl6@sunac.com.cn"  # 定义邮件发件人
text = "python is test smtp liuzhiliang"  # 邮件内容,编码为ASCII范围内的字符或字节字符串，所以不能写中文
BODY = '\r\n'.join((  # 组合sendmail方法的邮件主体内容，各段以"\r\n"进行分离
    "From: %s" % "admin",
    "TO: %s" % TO,
    "subject: %s" % SUBJECT,
    "",
    text
))
server = SMTP()  # 创建一个smtp对象
# server = smtplib.SMTP_SSL(HOST, 465)
server.connect(HOST, '25')  # 链接smtp主机
server.login("liuzl6", "****")  # 邮箱账号登陆
server.sendmail(FROM, TO, BODY)  # 发送邮件
server.quit()  # 关闭smtp链接
