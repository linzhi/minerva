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
import json
import traceback

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
        @return: urls: (['xxx', ['xxx']]); result: {'poi_id': xxx, 'name': xxx}
        """

        # 保存从content中提取的结果
        urls = None
        result = {}

        urls, content = HtmlParser.get_content(url=url)

        # 如果不是点评的店铺详情页的url，则退出
        poi_id = url.strip().split('/')[-1]
        if not poi_id.isdigit() or 'shop/' not in url:
            return urls, result

        try:
            if content:
                log.info('当前抓取的点评的店铺url是: {}'.format(url))

                # 解析名称，地址，电话
                name = content.find('h1', "shop-name").contents[0].strip().encode('utf8')
                address = content.find('span', itemprop='street-address').text.encode('utf8')
                phone = content.find('span', itemprop='tel').text.encode('utf8')
                result['poi_id'] = poi_id
                result['address'] = address
                result['name'] = name
                result['phone'] = phone
                result['src'] = 'dianping'
                result['url'] = url

                # 解析经纬度
                scripts = content.findAll('script')
                for script in scripts:
                    script = script.text.encode("utf8")
                    if "shop_config" in script:
                        for i in script.split(","):
                            if 'shopGlat' in i:
                                latitude = i.split(':')[-1].replace('"', '')
                                result['latitude'] = float(latitude)
                            if 'shopGlng' in i:
                                longitude = i.split(':')[-1].replace('"', '')
                                result['longitude'] = float(longitude)
                            if 'cityName' in i:
                                city = i.split(':')[-1].replace('"', '')
                                result['city'] = city
                        break
        except Exception as e:
            log.error('解析点评url: {} 异常，异常信息: {}'.format(url, traceback.format_exc()))
        finally:
            log.info('点评url:{}, 解析结果: {}'.format(url, result))
            return urls, result


if __name__ == "__main__":
    dianping = DianpingParser()
    dianping.get_poi_basic_info("http://www.dianping.com/shop/21171398")





