#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.connect import MysqlOper, idmquery
from datetime import datetime, timedelta
from libs.logger import errlog_org, infolog_org, debuglog_sys
import xml.etree.ElementTree as Et

CURRENT_DATE = datetime.today()
timestr = datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
idmid = 'AD_SUNAC_301_' + timestr
WSDL_URL = "http://esb.sunac.com.cn:8002/WP_SUNAC/APP_PUBLIC_SERVICES" \
           "/Proxy_Services/TA_IDM/PUBLIC_SUNAC_301_queryIdmOrgData_PS?wsdl"
TEST_WSDL_URL = "http://esbqas.sunac.com.cn:8001/WP_SUNAC/APP_PUBLIC_SERVICES" \
                "/Proxy_Services/TA_IDM/PUBLIC_SUNAC_301_queryIdmOrgData_PS?wsdl"
SYSTEMID = 'Sunac_IDMOrg'

