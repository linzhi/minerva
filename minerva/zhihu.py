# -*- coding:utf-8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
Created on 2017-04-19
Reference: https://github.com/xchaoinfo/fuck-login
"""

import BeautifulSoup
import json
import requests
import time
import datetime
import traceback

from conf import constant
from lib import log
from html_parser import HtmlParser


class ZhihuParser(HtmlParser):
    """
    @brief: 解析知乎的页面，获取高赞评论
    """

    INDEX_URL = constant.SEED_URL.ZHIHU
    LOGIN_URL = 'https://www.zhihu.com/login/email'
    CAPTCHA_URL = 'https://www.zhihu.com/captcha.gif?r='

    TIMEOUT = 20

    def __init__(self):
        if self.login('test', 'test'):
            log.info('模拟登陆知乎成功，开始抓取')
        else:
            raise Exception('模拟登陆知乎失败')

    def login(self, username, password):
        """
        @brief: 用户登录
        """

        login_result = False 
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Connection':'keep-alive'
        }

        try:
            _xsrf = BeautifulSoup.BeautifulSoup(session.get(self.INDEX_URL, headers=headers).content).find('input', {'name': '_xsrf'})['value']
        except Exception as e:
            log.error('获取知乎登陆的xsrf参数失败: {}'.format(traceback.format_exc()))
            return login_result

        captcha_url = self.CAPTCHA_URL + str(int(time.time()*1000)) + '&type=login'
        log.info('知乎登录的验证码url是: {}'.format(captcha_url))
        captcha = raw_input('请输入验证码：')

        data = {
            '_xrsf': _xsrf,
            'email': username,
            'password': password,
            'remember_me': 'true',
            'captcha': captcha
        }

        try:
            res = session.post(self.LOGIN_URL, headers=headers, data=data)
            if res.status_code == 200:
                res = res.json()
                if isinstance(res, dict) and 'errcode' in res and res.get('errcode') and 'msg' in res:
                    msg = res.get('msg').encode('utf8')
                    log.error('登录知乎账户失败,失败原因是: {}'.format(msg))
                # 登陆成功
                elif isinstance(res, dict) and 'errcode' in res and res.get('errcode') == 0:
                    login_result = True
                    print res
        except Exception as e:
            log.error('登录知乎失败, 异常信息: {}'.format(traceback.format_exc())) 

        return login_result

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
    zhihu = ZhihuParser()




