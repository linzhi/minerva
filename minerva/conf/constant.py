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

# Tornado服务器配置
TORNADO_SERVER_PORT = 8999

# 种子url
#SEED_URL = "http://www.zhihu.com/"
SEED_URL = "http://www.dianping.com/"

# Redis配置
REDIS_SERVER_HOST = "10.99.22.13"
REDIS_SERVER_PORT = 8107

# Redis定义key
KEY_URL = "crawled::url::{0}"

#Mongo配置
SPIDER_MONGO_ADDRESS = [{"host":"10.99.22.13", "port":8805}]
SPIDER_MONGO_DATABASE = "spider"
SPIDER_MONGO_USER = "test"
SPIDER_MONGO_PASSWD = "test"
SPIDER_MONGO_SOURCE_POI_TABLE = "source_url"




