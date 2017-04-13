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
from lib import utils
from thriftpy.rpc import make_client
from dianping import DianpingParser


class Spider(object):
    """
    @brief: 定向抓取
    """

    TIMEOUT = 50000

    def __init__(self):
        spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")
        self.master_spider = make_client(spider.SpiderService, '127.0.0.1', 8001, timeout=self.TIMEOUT)
        
        self.mongo_db = utils.MongoDBHandler(hosts=constant.SPIDER_MONGO_ADDRESS,
                                             db=constant.SPIDER_MONGO_DATABASE)

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
                log.error("保存的点评POI信息出现异常, poi info: {}".format(data))
        else:
            log.error("保存的点评POI信息缺少poi_id字段")

    def main(self):
        """
        @brief: Main
        """

        url = self.get_url()
        url = "http://www.dianping.com/shop/72066632"

        # 点评获取POI信息的接口返回的urls和poi_dict 2个参数,
        if url:
            urls, content = DianpingParser.get_poi_basic_info(url)
            if urls:
                self.send_url(urls)
            if content:
                self.save_dianping(content)


if __name__ == "__main__":
    spider = Spider()
    spider.main()

