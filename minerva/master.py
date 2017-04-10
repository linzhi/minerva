#!/usr/bin/env python2
# -*- coding = utf-8 -*-

################################################################################		
#		
# Copyright (c) 2017 linzhi. All Rights Reserved		
#		
################################################################################		

"""
spider
Created on 2017-04-08
Author: qilinzhi@gmail.com
"""

import os
import sys
import logging
import Queue
import traceback


from conf import constant
from lib import log
                 
class DispatchSpider(object):
    """
    spider dispatcher
    """

    def __init__(self):
        self.seed_url = constant.SEED_URL

    def __send_to_salve(self):
        pass

    def __receive_to_salve(self):
        pass

    def __get_from_queue(self):
        pass

    def __put_into_bloom_filter(self):
        pass

    def main(self):
        """
        @brief: Main
        """

        pass

if __name__ == "__main__":
    spider = DispatchSpider()
    spider.main()



