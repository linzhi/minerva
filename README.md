## Minerva 分布式爬虫

主要是有一些定制性的功能，作为平时使用的工具，其它的和传统型的分布式爬虫没啥区别

#### RPC
master和slave间方法调用采用Thrift RPC服务框架

#### 监控
待定

#### 存储
+ 待抓取的url存储在redis
+ 解析页面后的内容存储在mongo

#### 优点
+ master负责维护redis消息队列，slave扩容容易，只要新机器安装了python

#### 相关的依赖:
+ pymongo
+ redis
+ Scrapy
+ tornado
+ thriftpy


