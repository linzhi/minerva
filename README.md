## Minerva 分布式爬虫

主要是有一些定制性的功能，作为平时使用的工具，其它的和传统型的分布式爬虫没啥区别

#### 功能
+ 支持点评的POI数据抓取

#### 优点
+ master负责维护redis消息队列，slave扩容容易，只要新机器安装了python
+ master和slave间方法调用采用Thrift RPC服务框架,效率高

#### 存储
+ 已抓取的url存储在redis,待抓取的存储在master机器的内存中
+ 解析页面后的内容存储在mongo

#### 监控
待定

#### Usage:
+ 启动master: 
    python master.py

+ 启动slvae:
    python spider.py

#### 相关的依赖:
+ pymongo
+ redis
+ thriftpy
+ BeautifulSoup
+ chardet


