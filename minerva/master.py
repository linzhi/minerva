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
import sys
import Queue
import traceback
import thriftpy


from conf import constant
from lib import log
from lib import utils
from thriftpy.rpc import make_server

                 
class DispatchSpider(object):
    """
    spider dispatcher
    """

    CLIENT_TIMEOUT = 50000

    def __init__(self):
        self.seed_url = constant.SEED_URL

        self.redis_db = utils.RedisHandler(host=constant.REDIS_SERVER_HOST,
                                           port=constant.REDIS_SERVER_PORT)

        self.url_queue = Queue.Queue()
        self.url_queue.put(constant.KEY_URL.format(self.seed_url))

    def send_url(self):
        """
        @brief: 被slave调用，发送待抓取的url给slave节点
        """

        # 从url_queue中获取要抓取的url
        if self.url_queue.empty():
            log.error("抓取队列为空")
            raise RuntimeError("抓取队列为空")
        else:
            url = self.url_queue.get(True, 1)

        # 将抓取过的url写到redis
        res = self.redis_db.set(url, 1)
        if isinstance(res, dict) and res.get("errno") == 0 and res.get("data") is not None:
            log.info("已经抓取过的url: {} 写入redis成功".format(self.seed_url))
        else:
            log.error("已经抓取过的url写入redis异常, 异常信息: {}".format(traceback.format_exc()))
            raise RuntimeError("写入redis异常")

        return url

    def receive_url(self, urls=None):
        """
        @brief: 被slave调用，接收待抓取的url，并保存在Queue
        @return: Bool
        """

        # 需要return Ture，否则thriftpy会报Missing result
        if not urls: return True

        for url in urls:
            url = url.strip().encode('utf8')
            self.url_queue.put(url)

        log.info("当前待抓取的url总数为: {}".format(self.url_queue.qsize()))
        return True

    def main(self):
        """
        @brief: Main
        """

        spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")

        server = make_server(spider.SpiderService, DispatchSpider(), '127.0.0.1', 8001, client_timeout=self.CLIENT_TIMEOUT)
        server.serve()


if __name__ == "__main__":
    master = DispatchSpider()
    master.main()



