## Minerva

Minerva旨在提供**简单可依赖的分布式数据定向抓取工具**,目前已经实现的抓取功能有:
+ 定向抓取点评店铺详情页的POI数据,名称,地址,电话,城市,坐标

#### 特点
+ 使用redis存储linkbase信息:抓取url的FIFO队列由redis的list维护,已抓取url集合由redis的set维护
+ 页面解析存储在mongo,字段易存储、易扩展
+ spider可在多台机器单进程运行,充分利用机器资源
+ master和slave间方法调用采用Thrift RPC服务框架,效率高

#### Usage:
启动master: `python master.py`, 启动spider: `python spider.py`
配置文件为conf/constant.py, 可以修改服务的`ip/port`, 修改redis和mongo的地址

#### TODO:
+ 知乎高赞评论
+ 微博关键内容
+ 兼容点评的多种店铺页面
+ 支持url更新

#### 相关的依赖库:
+ pymongo (3.4.0)
+ redis (2.10.5)
+ thriftpy (0.3.9)
+ BeautifulSoup (3.2.1)
+ chardet (2.3.0)


