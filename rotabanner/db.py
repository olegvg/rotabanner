# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import redis

from rotabanner.config import redis_config as __redis_config


redis_client = redis.StrictRedis(host=__redis_config['host'], port=__redis_config['port'], db=__redis_config['db'])