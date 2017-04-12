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
import thriftpy
import traceback
import urllib
import urllib2
import urlparse

from conf import constant
from lib import log
from thriftpy.rpc import make_client


class HtmlParser(object):
    """
    @brief: 解析页面
    """

    TIMEOUT = 10

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

            for each_link in soup_context.findAll('a'):
                hyperlink = urlparse.urljoin(url, each_link.get('href'))
                hyperlinks.add(hyperlink)

            #for each_link in soup_context.findAll('img'):
            #    hyperlink = urlparse.urljoin(url, each_link.get('src'))
            #    hyperlinks.add(hyperlink)

        return hyperlinks, html_context


class Spider(object):
    """
    @brief: 
    """

    def __init__(self):
        self.html_parser = HtmlParser()

        spider = thriftpy.load(constant.THRIFT_FILE, module_name="spider_thrift")
        self.master_spider = make_client(spider.SpiderService, '127.0.0.1', 8001)

    def get_url(self):
        """
        @brief: 请求master，获取要抓取的url
        """
        
        url = ""
        try:
            url = self.master_spider.send_url()
            log.info("slave当前处理的url是: {}".format(url))
        except Exception as e:
            log.error("slave从master获取待抓取url异常, 异常信息: {}".format(traceback.format_exc()))
            raise RuntimeError("从master获取url失败")

        return url

    def send_url(self, urls=None):
        """
        @brief: 将后续待抓取的url发送给master
        """

        try:
            self.master_spider.receive_url(urls)
        except Exception as e:
            log.error("发送urls给master异常, 异常信息: {}".format(traceback.format_exc()))
            raise RuntimeError("slave发送urls到master失败")

    def main(self):
        url = self.get_url()

        urls, content = self.html_parser.get_hyperlinks(url)

        self.send_url(urls)


if __name__ == "__main__":
    demo = Spider()
    demo.main()

