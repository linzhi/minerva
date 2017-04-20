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
import cookielib
import json
import requests
import time
import traceback

from conf import constant
from lib import log
from html_parser import HtmlParser


class ZhihuParser(HtmlParser):
    """
    @brief: 解析知乎的页面，获取高赞评论
    """

    INDEX_URL = constant.SEED_URL['zhihu']
    LOGIN_URL = 'https://www.zhihu.com/login/email'
    CAPTCHA_URL = 'https://www.zhihu.com/captcha.gif?r='
    PROFILE_URL = "https://www.zhihu.com/settings/profile"

    TIMEOUT = 20

    def __init__(self):
        self.session = requests.Session()

        username = raw_input('请输入账户：')
        password = raw_input('请输入密码：')
        if self.login(username, password):
            log.info('模拟用户{}登陆知乎成功，开始抓取'.format(username))
        else:
            raise Exception('模拟用户{}登陆知乎失败'.format(username))

    def login(self, username, password):
        """
        @brief: 用户登录
        """

        login_result = False 
        self.session.cookies = cookielib.LWPCookieJar(filename='./conf/cookies')
        try:
            self.session.cookies.load(ignore_discard=True)
        except Exception as e:
            log.error("cookie 加载异常".format(traceback.format_exc()))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # 如果已经登录了，则不用再次登录
        res = self.session.get(self.PROFILE_URL, headers=headers, allow_redirects=False)
        if res.status_code == 200:
            login_result = True
            log.info('用户{}已经登录,无需再使用验证码登录'.format(username))
            return login_result

        try:
            _xsrf = BeautifulSoup.BeautifulSoup(self.session.get(self.INDEX_URL, headers=headers).content).find('input', {'name': '_xsrf'})['value']
        except Exception as e:
            log.error('获取知乎登陆的xsrf参数失败: {}'.format(traceback.format_exc()))
            return login_result

        try:
            captcha_url = self.CAPTCHA_URL + str(int(time.time() * 1000)) + '&type=login'
            img = self.session.get(captcha_url, headers=headers)
            if img.status_code == 200:
                with open('./conf/captcha.jpg', 'wb') as fd:
                    fd.write(img.content)
                    fd.close()
            else:
                return login_result
        except Exception as e:
            log.error('获取知乎登陆的验证码失败: {}'.format(traceback.format_exc()))
            return login_result

        captcha = raw_input('请输入验证码：')

        data = {
            '_xrsf': _xsrf,
            'email': username,
            'password': password,
            'remember_me': 'true',
            'captcha': captcha
        }

        try:
            res = self.session.post(self.LOGIN_URL, headers=headers, data=data)
            if res.status_code == 200:
                res = res.json()
                if isinstance(res, dict) and 'r' in res and res.get('r') and 'msg' in res:
                    msg = res.get('msg').encode('utf8')
                    log.error('登录知乎账户失败,失败原因是: {}'.format(msg))
                # 登陆成功,保存cookie
                elif isinstance(res, dict) and 'r' in res and res.get('r') == 0:
                    log.info('用户{}登录知乎成功，返回:{}'.format(username, res))
                    login_result = True
                    self.session.cookies.save()
        except Exception as e:
            log.error('登录知乎失败, 异常信息: {}'.format(traceback.format_exc())) 

        return login_result

    def get_zhihu_info(self, url):
        """
        @brief: 获取知乎的问题以及高赞的用户评论
        @return: urls: (['xxx', ['xxx']]); result: {'title': xxx, 'content': xxx}
        """

        # 保存从content中提取的结果
        urls = None
        result = {}

        urls, content = HtmlParser.get_content(url=url, session=self.session)
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
    zhihu.get_zhihu_info(url=constant.SEED_URL.ZHIHU)




