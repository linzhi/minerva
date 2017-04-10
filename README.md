### Minerva 分布式爬虫

主要是有一些定制性的功能，作为平时使用的工具，其它的和传统型的分布式爬虫没啥区别

##### RPC
master和slave间采用Thrift框架完成通信

##### 监控
待定

##### 优点
+ 配置容易

##### 相关的依赖:
+ pymongo
+ redis
+ Scrapy
+ tornado
+ thriftpy
