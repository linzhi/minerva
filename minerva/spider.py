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
import time
import thriftpy
import traceback

from conf import constant
from lib import log
from thriftpy.rpc import make_client
from html_parser import HtmlParser


class Spider(object):
    """
    @brief: 定向抓取
    """

    TIMEOUT = 50000

    def __init__(self):
        self.html_parser = HtmlParser()

        spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")
        self.master_spider = make_client(spider.SpiderService, '127.0.0.1', 8001, timeout=self.TIMEOUT)

    def get_url(self):
        """
        @brief: 请求master，获取要抓取的url
        """
        
        url = ""
        try:
            url = self.master_spider.send_url()
            log.info("slave当前处理的url是: {}".format(url))
        except Exception as e:
            log.error("slave从master获取待抓取url异常, 异常信息: {}".format(traceback.format_exc()))
            raise RuntimeError("从master获取url失败")

        return url

    def send_url(self, urls=None):
        """
        @brief: 将后续待抓取的url发送给master
        """

        try:
            # urls过多会引发异常，因此分批调用
            count = 0
            tmp_urls = set()
            for url in urls:
                count += 1
                tmp_urls.add(url)
                if count % 200 == 0:
                    self.master_spider.receive_url(tmp_urls)
                    tmp_urls.clear()
            if tmp_urls:
                self.master_spider.receive_url(tmp_urls)
        except Exception as e:
            log.error("发送urls给master异常, 异常信息: {}".format(traceback.format_exc()))
            raise RuntimeError("slave发送urls到master失败")

    def save_page(self):
        """
        @brief: 将需要的内容保存到mongo
        """

        pass

    def main(self):
        url = self.get_url()

        if url:
            urls, content = self.html_parser.get_hyperlinks(url)
            self.send_url(urls)


if __name__ == "__main__":
    spider = Spider()
    spider.main()

