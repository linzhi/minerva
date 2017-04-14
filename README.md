## Minerva 分布式爬虫

主要是有一些定制性的功能，作为平时使用的工具，其它的和传统型的分布式爬虫没啥区别

#### 功能
+ 支持点评店铺详情页的POI数据(名称，地址，电话)抓取,点评的POI数据存放`dianping_poi_info`表，唯一索引为`poi_id`

#### 优点
+ master和slave间方法调用采用Thrift RPC服务框架,效率高
+ 抓取后的数据由mongo存储，易扩展

#### 存储
+ 已抓取的url存储在redis，待抓取的存储在redis维护的FIFO队列中
+ 解析页面后的内容存储在mongo

#### Usage:
启动master: 

    python master.py

启动slave:

    python spider.py

#### 相关的依赖库:
+ pymongo (3.4.0)
+ redis (2.10.5)
+ thriftpy (0.3.9)
+ BeautifulSoup (3.2.1)
+ chardet (2.3.0)


