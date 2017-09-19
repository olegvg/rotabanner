# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'


import random
import re
import tornado.web
import tornado.gen
from db import redis_client
from config import tornado_config
from route import url_route
from init_db import init_db_from_csv


@url_route('/rotabanner')
class RotabannerHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine      # It doesn't need actually because redis-py cannot into coroutines
    def get(self):
        categories = [x for x in self.get_query_arguments('category') if re.search(r'^[\w\d]+$', x)]
        if len(categories) > 10:
            self.write('So much categories. Woof!')
            self.set_header('Content-Type', 'text/plain')
            self.set_status(400)        # Bad request
            self.finish()
            return
        while True:
            if len(categories) == 0:
                self.write('There is no banner to show. Bark!')
                self.set_header('Content-Type', 'text/plain')
                self.set_status(404)    # Not found
                self.finish()
                return
            current_category_idx = random.randint(0, len(categories) - 1)
            current_category = categories.pop(current_category_idx)
            cat_key = 'cat_{}'.format(current_category)

            while True:
                banner_id = redis_client.srandmember(cat_key)       # 'ban_<name>'
                if banner_id is None:
                    redis_client.delete(cat_key)
                    break
                banner_amount_key = '{}_amount'.format(banner_id)   # 'ban_<name>_amount'
                banner_amount = redis_client.get(banner_amount_key)
                if banner_amount is None or int(banner_amount) == 0:    # check banner_amount to prevent race condition
                    redis_client.delete(banner_amount_key)
                    redis_client.srem(cat_key, banner_id)
                else:
                    redis_client.decr(banner_amount_key)
                    templ_args = {
                        'dim_x': 720,
                        'dim_y': 90,
                        'base_uri': tornado_config['base_uri'],
                        'banner_name': re.search(r'ban_(.+)', banner_id).group(1)
                    }
                    self.render('banner.html', **templ_args)
                    return


@url_route('/init_db')
class InitDBHandler(tornado.web.RequestHandler):
    def get(self):
        init_db_from_csv()
        self.write('Redis db reinitialized with test data.')
        self.set_header('Content-Type', 'text/plain')


@url_route('/test')
class TestConnectionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Connection is ok!')
        self.set_header('Content-Type', 'text/plain')
        self.set_status(200)
