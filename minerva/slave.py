#!/usr/bin/env python2
# -*- coding = utf-8 -*-

################################################################################		
#		
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved		
#		
################################################################################		

"""
spider
Created on 2014-08-09
Author: qilinzhi@baidu.com
"""

import os
import sys

import BeautifulSoup
import chardet
import errno
import logging
import Queue
import re
import socket
import threading
import time
import traceback
import urllib
import urllib2
import urlparse

import exception
import log
import parse_conf


class HtmlParser(object):
    """get url context
    """

    def __init__(self):
        pass

    def parse_page(self, url, timeout):
        """get html content

           :param url: grab web
        """

        req = urllib2.Request(url=url)
        req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.1)')
        html_page = None

        try:
            response = urllib2.urlopen(req, timeout=timeout)
        except Exception as e:
            logging.error("parse html fail, url: {}, e: {}".format(url, traceback.format_exc()))
            return None
        else:
            html_page = response.read()
            response.close()
            try:
                encoding = chardet.detect(html_page)['encoding']
                if encoding and encoding != 'utf-8':
                    html_page = html_page.decode(encoding).encode('utf-8')
            except UnicodeDecodeError as e:
                logging.error("decode error, e: {}".format(traceback.format_exc()))
                return None
        
        return html_page

    def get_hyperlinks(self, url, timeout):
        """get all hyperlinks from url
        """

        html_context = self.parse_page(url, timeout)

        hyperlinks = []
        if html_context:
            soup_context = BeautifulSoup.BeautifulSoup(html_context)

            for each_link in soup_context.findAll('a'):
                hyperlink = urlparse.urljoin(url, each_link.get('href'))

                if hyperlink and ("javascript" not in hyperlink):
                    hyperlinks.append(hyperlink)

            for each_link in soup_context.findAll('img'):
                hyperlink = urlparse.urljoin(url, each_link.get('src'))

                if hyperlink and ("javascript" not in hyperlink):
                    hyperlinks.append(hyperlink)

        return set(hyperlinks), html_context


class CrawlerThread(threading.Thread):
    """
        multi thread crawl url
    """

    def __init__(self, arg_dict):
        """ 
            :param arg_dict: spider param
            :param crawl_links_queue: store crawl url queue 
        """ 

        self.arg_dict = arg_dict
        self.url_list_file = self.arg_dict["url_list_file"]
        self.max_depth = int(self.arg_dict["max_depth"])
        self.crawl_timeout = int(self.arg_dict["crawl_timeout"])
        self.crawl_interval = int(self.arg_dict["crawl_interval"])
        self.thread_count = int(self.arg_dict["thread_count"])
        self.output_directory = self.arg_dict["output_directory"]

        self.target_url = self.arg_dict["target_url"]
        self.target_url_re = re.compile(self.target_url)

        self.html_parser = HtmlParser()
        self.crawl_urls_queue = Queue.Queue()
        self.visited_urls = set()
        self.lock = threading.Lock()

    def main(self):
        """crawl spider main method
        """

        # get seed url, put into a queue and set depth is 0
        with open(str(self.url_list_file), "r") as url_file:
            for each_url in url_file:
                each_url = each_url.strip()
                self.visited_urls.add(each_url)
                self.crawl_urls_queue.put([each_url, 0])
   
        # creat dir to save match url
        if not os.path.exists(self.output_directory):
            try:
                os.makedirs(self.output_directory)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(self.output_directory):
                    pass
                else:
                    raise exception.MakeSaveDirException("fail,{}".format(self.output_directory))

        thread_pool = []
        for i in xrange(self.thread_count):
            thread = threading.Thread(target=self.crawl_url)
            thread.setDaemon(True)
            thread_pool.append(thread)

        for each_thread in thread_pool:
            each_thread.start()

        self.crawl_urls_queue.join()

        logging.info("crawl exc end!")
        return True

    def crawl_url(self):
        """
            bfs spider
        """

        while self.crawl_urls_queue.unfinished_tasks:
            try:
                url, url_depth = self.crawl_urls_queue.get(self.crawl_timeout)
            except Queue.Empty:
                time.sleep(0.1)
                continue

            thread_name = threading.currentThread().getName()
            logging.info("thread-name is: {}, url is: {}".format(thread_name, url))

            if url_depth > self.max_depth:
                self.crawl_urls_queue.task_done()
                continue

            hyperlinks, url_content = self.html_parser.get_hyperlinks(url, self.crawl_timeout)
            if self.target_url_re.match(url):
                file_path = os.path.join(self.output_directory, urllib.quote_plus(url))
                with open(file_path, 'w') as fd:
                    fd.write(url_content)

            for each_link in hyperlinks:
                if each_link in self.visited_urls:
                    continue
                self.lock.acquire()
                if each_link not in self.visited_urls:
                    self.crawl_urls_queue.put([each_link, url_depth + 1])
                    self.visited_urls.add(each_link)
                self.lock.release()

            time.sleep(self.crawl_interval)
            self.crawl_urls_queue.task_done()
                 

if __name__ == "__main__":
    log.init_log("./log/spider")

    args = parse_conf.parse_cmd()
    if args:
        arg_dict = parse_conf.parse_conf(args.conf_path)
    else:
        logging.error("parse cmd failed")
        sys.exit(1)

    if arg_dict:
        spider = CrawlerThread(arg_dict)
        spider.main()
    else:
        logging.error("load conf file failed")
        sys.exit(2)



