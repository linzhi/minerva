# encoding: utf-8

################################################################################
#
# Copyright (c) 2017 , All Rights Reserved
#
################################################################################


import pymongo
import redis


class MongoDBHandler(object):
    """
    @brief: 处理MongoDB操作
    @param hosts[in]: list 主机列表 [{"host":"127.0.0.1", "port":27017}]
    @param db[in]: str 数据库名
    @param repl[in]: str 集群名
    @param user[in]: str 用户名
    @param passwd[in]: str 密码
    """
    connPool = {}
    DEFAULT_RETRY_TIMES = 3
    
    
    def __init__(self, hosts, db='test', repl=None, user=None, passwd=None):
        self.repl = repl
        if self.repl is None:
            self.host = hosts[0]["host"]
            self.port = hosts[0]["port"]
        else:
            host_list = list()
            for host in hosts:
                host_list.append(host["host"] + ":" + str(host["port"]))
            self.host = ",".join(host_list)
            self.port = None
        self.user = user
        self.passwd = passwd
        self.db = db
        #self.conn = None
        self.conn_db = None
        self.conn_tbl = None
        self.connectDb()
        self.retry_times = MongoDBHandler.DEFAULT_RETRY_TIMES

    def connectDb(self):
        
        connKey = "%s_%s_%s_%s" % (self.host, self.port, self.db, self.repl)
        if connKey not in MongoDBHandler.connPool:
            self.reconnectDb(connKey)
        #else:
        #    if not MongoDBHandler.connPool[connKey].alive():
        #        self.reconnectDb(connKey)
        self.conn = MongoDBHandler.connPool[connKey]
        self.useDb(self.db, self.user, self.passwd)
    
    def reconnectDb(self, connKey):
        if self.repl is None:
            r = pymongo.MongoClient(host=self.host, port=self.port)
        else:
            r = pymongo.MongoReplicaSetClient(self.host, replicaSet=self.repl, \
                read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED)
        MongoDBHandler.connPool[connKey] = r
        
    def useDb(self, db_name, user=None, passwd=None):
        self.conn_db = getattr(self.conn, db_name)
        if user is not None:
            self.conn_db.authenticate(user, passwd)

    def useTbl(self, tbl_name):
        self.conn_tbl = getattr(self.conn_db, tbl_name)

    def upsert(self, criteria, data, tbl_name, is_set=False, upsert=True):
        """
        @brief: 向MongoDB upsert数据
        @param criteria[in]: dict 查询条件
        @param data[in]: dict 数据
        @param is_set[in]: True:覆盖，False:更新
        @param upsert[in]: True:有则更新，没有则插入，False:只更新
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """
        if not isinstance(tbl_name, basestring):
            return {"errno":1, "data":False, "errmsg":"tbl_name error"}
        for i in xrange(self.retry_times):
            try:
                self.useTbl(tbl_name)
                #if not self.conn.alive():
                #    self.connectDb()
                if is_set:
                    rslt = self.conn_tbl.update(criteria, data, upsert=upsert)
                else:
                    rslt = self.conn_tbl.update(criteria, {"$set":data}, upsert=upsert, multi=True)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno": 1, "data": False, "errmsg": "%s" % (ex)}
        return {"errno":0, "data":rslt, "errmsg":""}  

    def update(self, criteria, data, tbl_name):
        """
        @brief: 向MongoDB更新数据
        @param criteria[in]: dict 查询条件
        @param data[in]: dict 数据
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """
        if not isinstance(tbl_name, basestring):
            return {"errno":1, "data":False, "errmsg":"tbl_name error"}
        for i in xrange(self.retry_times):
            try:
                self.useTbl(tbl_name)
                if not self.conn.alive():
                    self.connectDb()
                rslt = self.conn_tbl.update(criteria, {"$set":data})
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":rslt, "errmsg":""}
    
    def insert(self, data, tbl_name):
        """
        @brief: 向MongoDB插入数据
        @param criteria[in]: dict 查询条件
        @param data[in]: dict 数据
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """
        if not isinstance(tbl_name, basestring):
            return {"errno":1, "data":False, "errmsg":"tbl_name error"}
        for i in xrange(self.retry_times):
            try:
                self.useTbl(tbl_name)
                #if not self.conn.alive():
                #    self.connectDb()
                rslt = self.conn_tbl.insert(data)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno": 1, "data": False, "errmsg": "%s" % (ex)}
        return {"errno":0, "data":rslt, "errmsg":""}
    
    def find(self, criteria, tbl_name, filter=None):
        """
        @brief: MongoDB读数据
        @param criteria[in]: dict 查询条件
        @param tbl_name[in]: 用到的表名
        @param filter[in]: dict 过滤条件,只定只查询哪些字段
        @return: dict {"errno":0, "data":data/False, "errmsg":""}
        """
        batch_size = 1000
        data_list = list()
        if not isinstance(tbl_name, basestring):
            return {"errno":1, "data":False, "errmsg":"tbl_name error"}
        for i in xrange(self.retry_times):
            try:
                self.useTbl(tbl_name)
                results = self.conn_tbl.find(criteria, filter).batch_size(batch_size)
                #if not self.conn.alive():
                #    self.connectDb()
                for r in results:
                    data_list.append(r)
                results.close()
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno": 1, "data": False, "errmsg": "%s" % (ex)}
        return {"errno":0, "data":data_list, "errmsg":""}
    
    def find_one(self, criteria, tbl_name, filter=None):
        """
        @brief: MongoDB读数据，读一条
        @param criteria[in]: dict 查询条件
        @param data[in]: dict 数据
        @param filter[in]: dict 过滤条件,只定只查询哪些字段
        @return: dict {"errno":0, "data":data/False, "errmsg":""}
        """
        if not isinstance(tbl_name, basestring):
            return {"errno":1, "data":False, "errmsg":"tbl_name error"}
        for i in xrange(self.retry_times):
            try:
                self.useTbl(tbl_name)
                #if not self.conn.alive():
                #    self.connectDb()
                rslt = self.conn_tbl.find_one(criteria, filter)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":rslt, "errmsg":""}
    
    def xfind(self, criteria, tbl_name, fields=None):
        """
        @brief: MongoDB读数据
        @param criteria[in]: dict 查询条件
        @param tbl_name[in]: 用到的表名
        @return: dict {"errno":0, "data":data/False, "errmsg":""}
        """
        if not isinstance(tbl_name, basestring):
            return {"errno":1, "data":False, "errmsg":"tbl_name error"}
        for i in xrange(self.retry_times):
            try:
                #if not self.conn.alive():
                #    self.connectDb()
                self.useTbl(tbl_name)
                if fields is not None:
                    results = self.conn_tbl.find(criteria, fields)
                else:
                    results = self.conn_tbl.find(criteria)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno": 1, "data": False, "errmsg": "%s" % (ex)}
        return {"errno":0, "data":results, "errmsg":"sucess"}
        
    #def __del__(self):
    #    if self.conn is not None:
    #        self.conn.close()


class RedisHandler(object):
    """
    @brief: 处理Redis操作
    """
    
    connPool = {}
    DEFAULT_RETRY_TIMES = 3
    
    def __init__(self, host, port):
        
        self.conn = None
        
        connKey = "%s:%s" % (host, port)
        if connKey not in RedisHandler.connPool:
            pool = redis.ConnectionPool(host=host, port=int(port))
            r = redis.StrictRedis(connection_pool=pool)
            RedisHandler.connPool[connKey] = r
        self.conn = RedisHandler.connPool[connKey]
        self.retry_times = RedisHandler.DEFAULT_RETRY_TIMES

    def __del__(self):
        pass

    def set(self, key, data, expireSeconds=None):
        """
        @brief: 设置Redis键对应的值
        @param key[in]: str Redis的键
        @param value[in]: object Redis的值
        @param expireSeconds[in]: Redis set的过期时间
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.set(key, data)
                if expireSeconds is not None and type(expireSeconds) == int:
                    self.conn.expire(key, expireSeconds)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}

    def delete(self, key):
        """
        @brief: 删除Redis键对应的值
        @param key[in]: str Redis的键
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.delete(key)
                break
            except Exception as ex:
                return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}
        
    def get(self, key):
        """
        @brief: 获取Redis键对应的值
        @param key[in]: str Redis的键
        @return: dict {"errno":0, "data":data/False, "errmsg":""}
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.get(key)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}

    def sadd(self, key, *value):
        """
        @brief: sadd
        @param key[in]: str Redis的键
        @param value[in]: object Redis的值
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.sadd(key, *value)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}
        
    def smembers(self, key):
        """
        @brief: smembers
        @param key[in]: str Redis的键
        @return: dict {"errno":0, "data":data/False, "errmsg":""}
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.smembers(key)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}

    def srem(self, key, value):
        """
        @brief: srem
        @param key[in]: str Redis的键
        @param value[in]: object Redis的值
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.srem(key, value)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}

    def rpush(self, key, value):
        """
        @brief: rpush
        @param key[in]: 队列名称
        @param value[in]: push到队列的value
        @return: dict {"errno":0, "data":True/False, "errmsg":""}, data为列表长度
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.rpush(key, value)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}

    def lpop(self, key):
        """
        @brief: lpop
        @param key[in]: 队列名称,从队列头部取数据
        @return: dict {"errno":0, "data":True/False, "errmsg":""}, data为从列表取出来的元素
        """

        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.lpop(key)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno":1, "data":False, "errmsg":"%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}

    def lrange(self, key):
        """
        @brief: lrange
        @param key[in]: str Redis的键
        @return: dict {"errno":0, "data":data/False, "errmsg":""}
        """
        if not isinstance(key, basestring):
            return {"errno":1, "data":False, "errmsg":"key error"}
        for i in xrange(self.retry_times):
            try:
                data = self.conn.lrange(key, start=0, end=-1)
                break
            except Exception as ex:
                if i == (self.retry_times - 1):
                    return {"errno": 1, "data": False, "errmsg": "%s" % (ex)}
        return {"errno":0, "data":data, "errmsg":""}
    
    def get_value(self, key, type="str"):
        """
        @brief: 返回Redis键对应的值
        @param key[in]: str Redis的键
        @param type[in]: class Redis的值的类型("str/set/list")
        @return: dict {"errno":0, "data":data/False, "errmsg":""}
        """
        if not isinstance(key, basestring) or (type != "str" and type != "set" and type != "list"):
            return {"errno": 1, "data": False, "errmsg": "parameter error"}
        if type == "str":
            return self.get(key)
        elif type == "set":
            return self.smembers(key)
        elif type == "list":
            return self.lrange(key)
            
    def set_value(self, key, value, type="str"):
        """
        @brief: 设置Redis键对应的值
        @param key[in]: str Redis的键
        @param value[in]: object Redis的值
        @param type[in]: class Redis的值的类型("str/set/list")
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """

        if not isinstance(key, basestring) or (type != "str" and type != "set" and type != "list"):
            return {"errno": 1, "data": False, "errmsg": "parameter error"}
        if not isinstance(value, basestring) and not isinstance(value, int) \
                and not isinstance(value, float) and not isinstance(value, dict) \
                and not isinstance(value, list):
            return {"errno": 1, "data": False, "errmsg": "parameter error"}
        if type == "str":
            return self.set(key, value)
        elif type == "set":
            self.delete(key)
            return self.sadd(key, value)
        elif type == "list":
            self.delete(key)
            return self.rpush(key, value)

    def add_value(self, key, value, type="str"):
        """
        @brief: 向Redis键对应的集合增加一个值
        @param key[in]: str Redis的键
        @param value[in]: object Redis的增加的值("str/set/list")
        @return: dict {"errno":0, "data":True/False, "errmsg":""}
        """

        if not isinstance(key, basestring) or (type != "str" and type != "set" and type != "list"):
            return {"errno": 1, "data": False, "errmsg": "parameter error"}
        if not isinstance(value, basestring) and not isinstance(value, int) \
                and not isinstance(value, float) and not isinstance(value, dict) \
                and not isinstance(value, list):
            return {"errno": 1, "data": False, "errmsg": "parameter error"}
        if type == "str":
            return self.set(key, value)
        elif type == "set":
            return self.sadd(key, value)
        elif type == "list":
            return self.rpush(key, value)
    
    
        
