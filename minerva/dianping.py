# -*- coding:utf-8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
Created on 2017-04-09
Author: qilinzhi@gmail.com
"""

import BeautifulSoup
import traceback

from conf import constant
from lib import log
from html_parser import HtmlParser


class DianpingParser(HtmlParser):
    """
    @brief: 解析点评的页面，获取POI数据
    """

    TIMEOUT = 20

    def __init__(self):
        pass

    @classmethod
    def get_poi_basic_info(cls, url):
        """
        @brief: 获取点评页面的POI信息
        @return: urls: (['xxx', ['xxx']]); result: {'poi_id': xxx, 'name': xxx}
        """

        # 保存从content中提取的结果
        urls = None
        result = {}

        urls, content = HtmlParser.get_content(url)

        # 如果不是点评的店铺详情页的url，则退出
        poi_id = url.strip().split('/')[-1]
        if not poi_id.isdigit():
            return urls, result

        try:
            if content:
                log.info("当前抓取的点评的店铺url是: {}".format(url))

                name = content.find('div', id='basic-info').h1.contents[0].strip().encode('utf8')
                address = content.find('span', itemprop='street-address').text.encode('utf8')
                phone = content.find('span', itemprop='tel').text.encode('utf8')
                log.info('点评url:{}, 解析结果 id:{}, name:{}, address:{}, phone:{}'.format(url, poi_id, name, address, phone))

                result['src'] = 'dianping'
                result['url'] = url
                result['poi_id'] = poi_id
                result['name'] = name
                result['address'] = address
                result['phone'] = phone

                return urls, result
        except Exception as e:
            log.error('解析url: {}异常，异常信息: {}'.format(url, traceback.format_exc()))

        return urls, result


if __name__ == "__main__":
    dianping = DianpingParser()
    dianping.get_poi_basic_info("http://www.dianping.com/shop/21171398")





