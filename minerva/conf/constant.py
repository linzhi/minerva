# encoding: utf-8

################################################################################
#
# Copyright (c) 2017 linzhi. All Rights Reserved
#
################################################################################

"""
@authors:  qilinzhi(qilinzhi@gmail.com)
@date:     2017年04月06日
"""


# 日志配置文件路径
LOG_CONFIG_PATH = "./conf/log.ini"
LOG_LOGGER_NAME = "spider"

# RPC配置
THRIFT_FILE = "./conf/spider.thrift"
RPC_HOST = "127.0.0.1"
RPC_PORT = 8001

# 种子url
SEED_URL = {
    "dianping": "http://www.dianping.com",
    "zhihu": "https://www.zhihu.com/question/56322619",
    "baidu": "http://www.baidu.com/"
}

# url类型
class URL_TYPE():
    DIANPING = "dianping"
    ZHIHU = "zhihu"

# Redis配置
REDIS_SERVER_HOST = "10.99.22.13"
REDIS_SERVER_PORT = 8107

# Redis定义key
DIANPING_LIST_URL_QUEUE = "dianping::url::queue"
DIANPING_CRAWLED_URL_SET = "dianping::crawled::url::set"

ZHIHU_LIST_URL_QUEUE = "zhihu::url::queue"
ZHIHU_CRAWLED_URL_SET = "zhihu::crawled::url::set"

#Mongo配置
SPIDER_MONGO_ADDRESS = [{"host":"10.99.22.13", "port":8805}]
SPIDER_MONGO_DATABASE = "spider"
SPIDER_MONGO_USER = "test"
SPIDER_MONGO_PASSWD = "test"
SPIDER_MONGO_DIANPING_POI_TABLE = "dianping_poi_info"
SPIDER_MONGO_ZHIHU_POI_TABLE = "zhihu_info"




