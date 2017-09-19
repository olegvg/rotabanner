# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'


import csv
from rotabanner.db import redis_client


def init_db_from_csv():
    with open('./testdata.csv') as csv_file:
        csv_obj = csv.reader(csv_file, delimiter=';')
        for row in csv_obj:
            banner_name = row[0]
            amount = row[1]
            del row[:2]
            categories = row[:10]

            banner_amount_key = 'ban_{}_amount'.format(banner_name)
            redis_client.set(banner_amount_key, amount)

            banner_key = 'ban_{}'.format(banner_name)
            for category in categories:
                category_key = 'cat_{}'.format(category)
                redis_client.sadd(category_key, banner_key)
