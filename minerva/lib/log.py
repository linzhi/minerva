# encoding: utf-8

################################################################################
#
# Copyright (c) 2017 linzhi. All Rights Reserved
#
################################################################################

"""
Created on 2017-04-06
Author: linzhi
"""

import logging.config

from conf import constant


logging.config.fileConfig(constant.LOG_CONFIG_PATH)
logger = logging.getLogger(constant.LOG_LOGGER_NAME)

info = logger.info
error = logger.error
warning = logger.warning
debug = logger.debug
