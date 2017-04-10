# -*- coding:utf8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
Created on 2017-04-08
Author: qilinzhi@gmail.com
"""

import os
import Queue
import traceback
import thriftpy


from conf import constant
from lib import log
from lib import DbUtils
from thriftpy.rpc import make_server

                 
class DispatchSpider(object):
    """
    spider dispatcher
    """

    def __init__(self):

        self.seed_url = constant.SEED_URL

        self.redis_db = DbUtils.RedisHandler(host=constant.REDIS_SERVER_HOST, 
                                             port=constant.REDIS_SERVER_PORT)

    def send_to_slave(self, url=None):
        """
        @brief: 被slave调用，发送待抓取的url给slave节点
        """

        return 111100

    def receive_from_slave(self, url=None):
        """
        @brief: 被slave调用，接收待抓取的url，并保存在redis
        """
        pass

    def __get_url_from_reids(self):
        """
        @brief: 从redis中获取要下发给slave机器的url
        @return: url: 未被抓取过的url
        """

        pass

    def __put_url_into_redis(self):
        """
        @brief: 把slave机器返回的待抓取的url写到redis
        """

        pass

    def __set_url_to_bf(self):
        """
        @brief: 使用布隆滤波器保存抓取过的url，做去重
        """

        pass

    def main(self):
        """
        @brief: Main
        """

        pass

def main():
    """
    @brief: 
    """

    spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")

    server = make_server(spider.SpiderService, DispatchSpider(), '127.0.0.1', 8001)
    log.info('master serving...')
    server.serve()


if __name__ == "__main__":
    main()



