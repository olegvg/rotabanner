# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'


import os
from config import tornado_config
from route import url_handlers
import tornado.web
import tornado.ioloop
import tornado.httpserver
import endpoint


def get_app():
    is_debug = tornado_config['debug']
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    return tornado.web.Application(url_handlers, debug=is_debug, autoreload=is_debug, template_path=template_path)


def run_server():
    host = tornado_config['host']
    port = tornado_config['port']
    proc_num = tornado_config['proc_num']
    app = get_app()

    server = tornado.httpserver.HTTPServer(app)
    server.bind(port, host)

    is_debug = tornado_config['debug']
    if is_debug is not True:
        server.start(proc_num)
    else:
        server.start()

    tornado.ioloop.IOLoop.current().start()