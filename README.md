## Minerva

使用python开发的分布式爬虫,目前已经实现的抓取功能有:
+ 定向抓取点评店铺详情页的POI数据,名称,地址,电话

#### 优点
+ master和slave间方法调用采用Thrift RPC服务框架,效率高
+ 抓取结果由mongo存储,易扩展

#### 存储
+ 已抓取的url存储在redis,待抓取的存储在redis维护的FIFO队列中
+ 解析页面后的内容存储在mongo

####TODO:
+ 去掉python chardet库的依赖

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


