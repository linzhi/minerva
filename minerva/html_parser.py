# -*- coding:utf-8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
Created on 2017-04-09
Author: linzhi
"""

import BeautifulSoup
import chardet
import traceback
import requests
import urlparse

from conf import constant
from lib import log


class HtmlParser(object):
    """
    @brief: 解析页面
    """

    TIMEOUT = 20

    def __init__(self):
        pass

    @classmethod
    def parse_page(cls, url=None, session=None):
        """
        @brief: get html content
        """

        html_page = None
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }

        try:
            if session:
                response = session.get(url=url, headers=headers)
                if response.status_code == requests.codes.ok:
                    html_page = response.text
            else:
                response = requests.get(url=url, headers=headers)
                if response.status_code == requests.codes.ok:
                    html_page = response.text
        except Exception as e:
            log.error("解析网页异常, url: {}, e: {}".format(url, traceback.format_exc()))
        
        return html_page

    @classmethod
    def get_content(cls, url=None, session=None):
        """
        @brief: 解析url，获取页面链接和页面内容
        """

        hyperlinks = set()
        soup_context = None

        # 解析网页获取网页链接和网页内容
        html_context = cls.parse_page(url, session)
        if html_context:
            soup_context = BeautifulSoup.BeautifulSoup(html_context)
            if soup_context:
                soup_context = BeautifulSoup.BeautifulSoup(html_context)
                for each_link in soup_context.findAll('a'):
                    hyperlink = urlparse.urljoin(url, (each_link or {}).get('href'))
                    hyperlinks.add(hyperlink)

        return hyperlinks, soup_context


if __name__ == "__main__":
    pass
