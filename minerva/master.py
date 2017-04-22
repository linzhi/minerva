# -*- coding:utf8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
Created on 2017-04-08
Author: linzhi
"""

import os
import sys
import Queue
import thriftpy
import hashlib

from conf import constant
from lib import log
from lib import utils
from thriftpy.rpc import make_server

                 
class DispatchSpider(object):
    """
    spider dispatcher
    """


    def __init__(self):

        self.redis_db = utils.RedisHandler(host=constant.REDIS_SERVER_HOST,
                                           port=constant.REDIS_SERVER_PORT)

        self.seed_url = constant.SEED_URL.values()

        # 将点评种子url写到redis队列
        res = self.redis_db.rpush(constant.DIANPING_LIST_URL_QUEUE, constant.SEED_URL['dianping'])
        if isinstance(res, dict) and 'errno' in res and res['errno'] != 0 and 'errmsg' in res:
            errmsg = res['errmsg']
            log.error("初始化seed url失败, error msg: {}".format(errmsg))

        # 将知乎种子url写到redis队列
        res = self.redis_db.rpush(constant.ZHIHU_LIST_URL_QUEUE, constant.SEED_URL['zhihu'])
        if isinstance(res, dict) and 'errno' in res and res['errno'] != 0 and 'errmsg' in res:
            errmsg = res['errmsg']
            log.error("初始化seed url失败, error msg: {}".format(errmsg))

    def send_url(self, url_type='dianping'):
        """
        @brief: 被slave调用，发送待抓取的url给slave节点
        @return: 如果获取的url已经抓取过，那么返回 "", 否则返回url
        @param: url_type是抓取的网站类型，比如'dianping' or 'zhihu',默认是'dianping'
        """

        if url_type == constant.URL_TYPE.DIANPING:
            redis_list_key = constant.DIANPING_LIST_URL_QUEUE
            redis_set_key = constant.DIANPING_CRAWLED_URL_SET
        elif url_type == constant.URL_TYPE.ZHIHU:
            redis_list_key = constant.ZHIHU_LIST_URL_QUEUE
            redis_set_key = constant.ZHIHU_CRAWLED_URL_SET
        else:
            log.error('url_type is errro')
            raise Exception('url_type is errro')

        # 从redis队列中获取要抓取的url
        res = self.redis_db.lpop(redis_list_key) 
        if isinstance(res, dict) and 'errno' in res and res['errno'] == 0 and \
            'data' in res and res['data'] is not None:
            url = res['data']
        elif 'errmsg' in res:
            errmsg = res['errmsg']
            log.error("redis队列{}中获取待取的url失败, errmsg: {}".format(redis_list_key, errmsg))
            raise RuntimeError("redis队列{}中获取待抓取的url失败".format(redis_list_key))

        # 判断非种子url是否已经抓取过，如果抓取过返回空，没有则写入redis的去重队列
        value = hashlib.md5(url).hexdigest()
        if url not in self.seed_url:
            res = self.redis_db.sismember(redis_set_key, value)
            if isinstance(res, dict) and res.get("errno") == 0 and res.get("data") > 0:
                log.info("redis的集合{}的url: {} 已经抓取过，不再返回".format(redis_set_key, url))
                return ""

        res = self.redis_db.sadd(redis_set_key, value)
        if isinstance(res, dict) and 'errno' in res and res.get("errno") == 0:
            log.info("已经抓取的url: {} 写入redis集合{} 成功".format(url, redis_set_key))
        elif isinstance(res, dict) and res.get("errmsg") is not None:
            errmsg = res.get('errmsg')
            log.error("已经抓取的url: {} 写入redis集合{} 异常, errmsg: {}".format(url, redis_set_key, errmsg))
            raise RuntimeError("已经抓取过的url写入redis集合{} 异常".format(redis_set_key))

        return url

    def receive_url(self, urls=None, url_type='dianping'):
        """
        @brief: 被slave调用，接收待抓取的url，并保存在Queue
        @param: url_type是抓取的网站类型，比如'dianping' or 'zhihu',默认是'dianping'
        @return: Bool
        """

        # 需要return Ture，否则thriftpy会报Missing result
        if not urls: return True

        # 根据url_type 选择往哪个redis队列写数据
        if url_type == constant.URL_TYPE.DIANPING:
            redis_list_key = constant.DIANPING_LIST_URL_QUEUE
        elif url_type == constant.URL_TYPE.ZHIHU:
            redis_list_key = constant.ZHIHU_LIST_URL_QUEUE
        else:
            log.error('url_type is errro')
            raise Exception('url_type is errro')

        for url in urls:
            url = url.strip().encode('utf8')
            res = self.redis_db.rpush(redis_list_key, url)
            if isinstance(res, dict) and 'errno' in res and res.get('errno') != 0 and 'errmsg' in res:
                errmsg = res.get('errmsg')
                log.error("写url :{} 到redis队列{}失败, error msg: {}".format(url, redis_list_key, errmsg))

        return True

def main():
    """
    @brief: Main
    """

    CLIENT_TIMEOUT = 50000

    spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")
    server = make_server(spider.SpiderService, DispatchSpider(), constant.RPC_HOST, 
                             constant.RPC_PORT, client_timeout=CLIENT_TIMEOUT)
    server.serve()


if __name__ == "__main__":
    main()



