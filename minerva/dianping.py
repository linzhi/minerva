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

import os
import BeautifulSoup
import chardet
import traceback
import urllib
import urllib2
import urlparse

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
        @return: urls: (['xxx', ['xxx']]); poi_dict: {'poi_id': xxx, 'name': xxx}
        """

        # 如果不是点评的店铺详情页的url，则退出
        poi_id = url.strip().split('/')[-1]
        if not poi_id.isdigit():
            return None

        urls, content = HtmlParser.get_content(url)
        try:
            if content:
                poi_dict = {}
                name = content.find('div', id='basic-info').h1.text.encode('utf8').rstrip('添加分店')
                address = content.find('span', itemprop='street-address').text.encode('utf8')
                phone = content.find('span', itemprop='tel').text.encode('utf8')
                log.info('url:{}, 解析的id:{}, name:{}, address:{}, phone:{}'.format(url, poi_id, name, address, phone))

                poi_dict['id'] = poi_id
                poi_dict['name'] = name
                poi_dict['address'] = address
                poi_dict['phone'] = phone

                return urls, poi_dict
        except Exception as e:
            log.error('解析url: {}异常，异常信息: {}'.format(url, traceback.format_exc()))
            return None


if __name__ == "__main__":
    dianping = DianpingParser()
    dianping.get_poi_basic_info("http://www.dianping.com/shop/72066632")





