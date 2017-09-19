# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from rotabanner import init_db
from rotabanner import app

if __name__ == '__main__':
    init_db.init_db_from_csv()
    app.run_server()
