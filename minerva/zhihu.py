# -*- coding:utf-8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
Created on 2017-04-19
Author: qilinzhi@gmail.com
"""

import BeautifulSoup
import json
import traceback

from conf import constant
from lib import log
from html_parser import HtmlParser


class ZhihuParser(HtmlParser):
    """
    @brief: 解析知乎的页面，获取高赞评论
    """

    TIMEOUT = 20

    def __init__(self):
        pass

    def is_login(self):
        """
        @brief: 判断用户是否登录
        """

        pass

    @classmethod
    def get_info(cls, url):
        """
        @brief: 获取知乎的问题以及高赞的用户评论
        @return: urls: (['xxx', ['xxx']]); result: {'title': xxx, 'content': xxx}
        """

        # 保存从content中提取的结果
        urls = None
        result = {}

        urls, content = HtmlParser.get_content(url)

        try:
            if content:
                log.info("当前抓取的知乎url是: {}".format(url))
        except Exception as e:
            log.error('解析知乎url: {} 异常，异常信息: {}'.format(url, traceback.format_exc()))
        finally:
            log.info('知乎url:{}, 解析结果: {}'.format(url, result))
            return urls, result


if __name__ == "__main__":
    pass




