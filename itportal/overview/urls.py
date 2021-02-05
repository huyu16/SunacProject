#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'overview'

urlpatterns = [
    path('', views.index, name='index'),
    path('host_monitordata', views.host_monitordata, name='host_monitordata'),
    path('user_expire', views.user_expire, name='user_expire')
]
