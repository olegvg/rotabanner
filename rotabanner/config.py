# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import yaml
import logging


redis_config = {}
tornado_config = {}

with open('rotabanner_config.yml') as config_file:
    config = yaml.load(config_file)

    _rotabanner_logger = logging.getLogger('tornado.application.rotabanner')

    try:
        service_log_level = config['rotabanner']['logger']['level']
        _rotabanner_logger.setLevel(service_log_level)
    except (KeyError, TypeError):
        _rotabanner_logger.error("'config:rotabanner.logger.level' not found or incorrect, "
                                 "beware and check your config!")

    service_log_handler = logging.StreamHandler()
    try:
        service_log_format = config['rotabanner']['logger']['format']
        service_formatter = logging.Formatter(service_log_format)
        service_log_handler.setFormatter(service_formatter)
    except (KeyError, TypeError):
        _rotabanner_logger.error("'config:rotabanner.logger.format' not found or incorrect, "
                                 "beware and check your config!")

    _rotabanner_logger.addHandler(service_log_handler)

    try:
        redis_config['host'] = config['rotabanner']['redis']['host']
        redis_config['port'] = config['rotabanner']['redis']['port']
        redis_config['db'] = int(config['rotabanner']['redis']['db'])
    except (KeyError, TypeError):
        _rotabanner_logger.error("'config:rotabanner.redis' not found or incorrect, beware and check your config!")

    try:
        tornado_config['host'] = config['rotabanner']['tornado']['host']
        tornado_config['port'] = int(config['rotabanner']['tornado']['port'])
        tornado_config['debug'] = bool(config['rotabanner']['tornado']['debug'])
        tornado_config['proc_num'] = int(config['rotabanner']['tornado']['proc_num'])
        tornado_config['base_uri'] = config['rotabanner']['tornado']['base_uri']
    except (KeyError, TypeError):
        _rotabanner_logger.error("'config:rotabanner.tornado' not found or incorrect, beware and check your config!")