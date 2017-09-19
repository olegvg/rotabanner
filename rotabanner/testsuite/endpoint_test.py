# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import re
from rotabanner.testsuite import TestHandlerBase


class EndpointTestHandler(TestHandlerBase):
    def connection_test(self):
        response = self.fetch('/test', method='GET')
        self.assertEqual(response.code, 200)

    def flight_category_test(self):
        banners_score = {}
        while True:
            response = self.fetch('/rotabanner?category=flight', method='GET')
            if response.code != 200:
                break
            idx = int(re.search(r'banner(\d+?)\.jpg', response.body).group(1))
            banners_score.setdefault(idx, 0)
            banners_score[idx] += 1
        self.assertEqual(len(banners_score.items()), 3)
        self.assertSequenceEqual(banners_score.values(), [10, 10, 10])

    def aviation_category_exhaustion_test(self):
        while True:
            response = self.fetch('/rotabanner?category=flight', method='GET')
            if response.code != 200:
                break

        aviation_uri = '/rotabanner?category=aviation'
        for _ in xrange(0, 9):
            self.fetch(aviation_uri, method='GET')

        response = self.fetch(aviation_uri, method='GET')
        self.assertEqual(response.code, 200)

        response = self.fetch(aviation_uri, method='GET')
        self.assertEqual(response.code, 404)

    def mix_categories_exhaustion_test(self):
        mix_uri = '/rotabanner?category=fly&category=grasshopper'

        for _ in xrange(0, 19):
            self.fetch(mix_uri, method='GET')

        response = self.fetch(mix_uri, method='GET')
        self.assertEqual(response.code, 200)

        response = self.fetch(mix_uri, method='GET')
        self.assertEqual(response.code, 404)
