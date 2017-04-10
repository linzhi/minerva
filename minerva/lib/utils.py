# encoding: utf-8

################################################################################
#
# Copyright (c) 2017 linzhi. All Rights Reserved
#
################################################################################

"""
@authors:  qilinzhi(qilinzhi@gmail.com)
@date:     2017年04月07日
"""

import redis
import pymongo


class RedisHelper(object):
    
    _conn_pool = None
    
    @staticmethod
    def init(**kwargs):
        RedisHelper._conn_pool = redis.ConnectionPool(**kwargs)
    
    @staticmethod
    def get_connection():
        return redis.StrictRedis(connection_pool=RedisHelper._conn_pool)
    

class MongoHelper(object):
    
    @staticmethod
    def get_connection(hosts,  **kwargs):
        if "replicaSet" in kwargs:
            return pymongo.MongoReplicaSetClient(hosts, **kwargs)
        else:
            return pymongo.MongoClient(hosts, **kwargs)
