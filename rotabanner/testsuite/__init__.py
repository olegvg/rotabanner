# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'


import os

test_confs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'testing')
os.chdir(test_confs_dir)

from tornado.testing import AsyncHTTPTestCase
from rotabanner.app import get_app
from rotabanner.db import redis_client
from rotabanner.init_db import init_db_from_csv


class TestHandlerBase(AsyncHTTPTestCase):
    def setUp(self):
        redis_client.flushall()
        init_db_from_csv()

        super(TestHandlerBase, self).setUp()

    def get_app(self):
        return get_app()
