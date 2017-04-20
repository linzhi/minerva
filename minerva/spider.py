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
import hashlib
import time
import thriftpy
import traceback

from conf import constant
from lib import log
from lib import utils
from thriftpy.rpc import make_client
from dianping import DianpingParser
from zhihu import ZhihuParser


class Spider(object):
    """
    @brief: 定向抓取
    """

    TIMEOUT = 50000

    def __init__(self):
        spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")
        self.master_spider = make_client(spider.SpiderService, constant.RPC_HOST, 
                                         constant.RPC_PORT, timeout=self.TIMEOUT)
        
        self.mongo_db = utils.MongoDBHandler(hosts=constant.SPIDER_MONGO_ADDRESS,
                                             db=constant.SPIDER_MONGO_DATABASE)

    def get_url(self, url_type='dianping'):
        """
        @brief: 请求master的send_url接口获取下一个要抓取的url
        @param: ulr_type 代表获取dianping的还是zhihu的url,默认值是dianping
        """
        
        url = ""
        try:
            url = self.master_spider.send_url(url_type=url_type)
            if url:
                log.info("从master获取到{}的url是: {}".format(url_type, url))
            else:
                return url
        except Exception as e:
            log.error("从master获取{}待抓取的url异常, 异常信息: {}".format(url_type, traceback.format_exc()))

        return url

    def send_url(self, urls=None, url_type='dianping'):
        """
        @brief: 将后续待抓取的url发送给master
        @param: ulr_type 代表获取dianping的还是zhihu的url,默认值是dianping
        """

        try:
            count = 0
            tmp_urls = set()
            for url in urls:
                count += 1
                tmp_urls.add(url)
                if count % 200 == 0:
                    self.master_spider.receive_url(urls=tmp_urls, url_type=url_type)
                    tmp_urls.clear()
            if tmp_urls:
                self.master_spider.receive_url(urls=tmp_urls, url_type=url_type)
        except Exception as e:
            log.error("发送urls给master异常, 异常信息: {}".format(traceback.format_exc()))

    def save_dianping(self, data=None):
        """
        @brief: 将需要的点评的json格式POI数据保存到mongo
        """

        if data is None: return None

        if 'poi_id' in data:
            key = {}
            key['poi_id'] = data['poi_id']

            ret = self.mongo_db.upsert(key, data, constant.SPIDER_MONGO_DIANPING_POI_TABLE)
            if isinstance(ret, dict) and 'errno' in ret and ret['errno'] != 0:
                log.error("保存点评POI信息出现异常, poi info: {}".format(data))
        else:
            log.error("保存的点评POI信息缺少poi_id字段")

    def run(self):
        """
        @brief: Run Spider
        """

        while 1:
            # 抓取点评的信息
            url_type = 'dianping'
            url = self.get_url(url_type=url_type)
            try:
                if url:
                    # 获取要抓取的url的超链接和内容
                    urls, result = DianpingParser.get_poi_basic_info(url)
                    if urls:
                        self.send_url(urls, url_type=url_type)
                    if result:
                        self.save_dianping(result)
            except Exception as e:
                log.error("抓取{}的url: {} 异常: {}".format(url_type, url, traceback.format_exc()))
                continue

            # 抓取知乎的信息


if __name__ == "__main__":
    spider = Spider()
    spider.run()

