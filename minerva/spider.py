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
import traceback

from conf import constant
from lib import log
from thriftpy.rpc import make_client

spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")
master_spider = make_client(spider.SpiderService, '127.0.0.1', 8001)


class HtmlParser(object):
    """
    @brief: 解析页面
    """

    def __init__(self):
        pass


class Spider(object):
    """
    @brief: 
    """

    def __init__(self):
        pass

    def main(self):
        # 从master机器获取要抓取的url
        try:
            url = master_spider.send_to_slave()
            log.info("slave当前抓取的url是: {}".format(url))
        except Exception as e:
            log.info("slave从master获取待抓取url异常, 异常信息: {}".format(traceback.format_exc()))


if __name__ == "__main__":
    demo = Spider()
    demo.main()

