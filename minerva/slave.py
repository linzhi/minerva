# -*- coding:utf-8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
Created on 2017-04-09
Author: qilinzhi@gmail.com
"""

import os
import thriftpy

from conf import constant
from lib import log
from thriftpy.rpc import make_client


if __name__ == "__main__":
    spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")

    master_spider = make_client(spider.SpiderService, '127.0.0.1', 8001)
    master_spider.send_to_slave()

