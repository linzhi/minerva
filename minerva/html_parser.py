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
import chardet
import traceback
import urllib
import urllib2
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
    def parse_page(cls, url):
        """
        @brief: get html content
        """

        html_page = None
        req = urllib2.Request(url=url)
        req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.1)')

        try:
            response = urllib2.urlopen(req, timeout=cls.TIMEOUT)
        except Exception as e:
            log.error("解析网页异常, url: {}, e: {}".format(url, traceback.format_exc()))
        else:
            html_page = response.read()
            response.close()
            try:
                encoding = chardet.detect(html_page)['encoding']
                if encoding and encoding != 'utf-8':
                    html_page = html_page.decode(encoding).encode('utf-8')
            except UnicodeDecodeError as e:
                log.error("网页解码异常, e: {}".format(traceback.format_exc()))
        
        return html_page

    @classmethod
    def get_content(cls, url):
        """
        @brief: 解析url，获取页面链接和页面内容
        """

        hyperlinks = set()
        soup_context = None

        # 解析网页获取网页链接和网页内容
        html_context = cls.parse_page(url)
        if html_context:
            soup_context = BeautifulSoup.BeautifulSoup(html_context)
            if soup_context:
                soup_context = BeautifulSoup.BeautifulSoup(html_context)
                for each_link in soup_context.findAll('a'):
                    hyperlink = urlparse.urljoin(url, each_link.get('href'))
                    hyperlinks.add(hyperlink)

        return hyperlinks, soup_context


if __name__ == "__main__":
    pass
