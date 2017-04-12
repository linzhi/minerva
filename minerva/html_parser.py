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


class HtmlParser(object):
    """
    @brief: 解析页面
    """

    TIMEOUT = 20

    def __init__(self):
        pass

    def parse_page(self, url):
        """
        @brief: get html content
        """

        req = urllib2.Request(url=url)
        req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.1)')
        html_page = None

        try:
            response = urllib2.urlopen(req, timeout=self.TIMEOUT)
        except Exception as e:
            log.error("parse html fail, url: {}, e: {}".format(url, traceback.format_exc()))
            return None
        else:
            html_page = response.read()
            response.close()
            try:
                encoding = chardet.detect(html_page)['encoding']
                if encoding and encoding != 'utf-8':
                    html_page = html_page.decode(encoding).encode('utf-8')
            except UnicodeDecodeError as e:
                log.error("decode error, e: {}".format(traceback.format_exc()))
                return None
        
        return html_page

    def get_hyperlinks(self, url):
        """
        @brief: 解析url，获取超链接和url内容
        @return: 返回超链接和url的内容
        """

        html_context = self.parse_page(url)

        hyperlinks = set()
        if html_context:
            soup_context = BeautifulSoup.BeautifulSoup(html_context)

            # 获取其他站点链接 
            for each_link in soup_context.findAll('a'):
                hyperlink = urlparse.urljoin(url, each_link.get('href'))
                hyperlinks.add(hyperlink)

            # 获取图片链接
            #for each_link in soup_context.findAll('img'):
            #    hyperlink = urlparse.urljoin(url, each_link.get('src'))
            #    hyperlinks.add(hyperlink)

        return hyperlinks, html_context


if __name__ == "__main__":
    pass
