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
    def get_poi_info(cls, url):
        urls, content = HtmlParser.get_content(url)
        return content


if __name__ == "__main__":
    dianping = DianpingParser()
    print dianping.get_poi_info("http://www.dianping.com/shop/22974252")





