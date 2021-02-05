#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,json,os
from datetime import datetime,timedelta
from envelopes import Envelope

def send_mail(mail_body,mail_addr):
    from_addr = 'eop0003@sunac.com.cn'
    to_addr = mail_addr
    # 以QQ邮箱为例，密码需要为smtp服务授权码
    passwords = 'Abcd1234'
    sever = 'mail.sunac.com.cn'
    # 主题(subject)与内容(content)
    subject = '批量邮件发送实验'
    text_body = mail_body
    msg=Envelope(to_addr=to_addr,from_addr=from_addr,subject=subject,text_body=text_body)
    msg.send(sever,login=from_addr,password=passwords,tls=True)

send_mail("pi liang fasong shi yan","huy33@sunac.com.cn")