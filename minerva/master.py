#!/usr/bin/env python2
# -*- coding = utf-8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
spider
Created on 2017-04-08
Author: qilinzhi@gmail.com
"""

import os
import sys
import logging
import Queue
import traceback

from conf import constant
from lib import log

                 
class DispatchSpider(object):
    """
    spider dispatcher
    """

    def __init__(self):
        self.seed_url = constant.SEED_URL

        self.redis_db = DbUtils.RedisHandler(host=constants.REDIS_SERVER_HOST, 
                                             port=constants.REDIS_SERVER_PORT)

    def send_to_salve(self, url=None):
        """
        @brief: 被slave调用，发送url给slave节点
        """

        pass

    def receive_from_salve(self, url=None):
        """
        @brief: 被slave调用，接收待抓取的ur，并保存在redis
        """

        pass

    def __get_url_from_reids(self):
        """
        @brief: 从redis中获取要下发给slave机器的url
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

if __name__ == "__main__":
    spider = DispatchSpider()
    spider.main()



