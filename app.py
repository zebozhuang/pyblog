#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('..')

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.autoreload

from tornado.options import define, options
from pyblog.settings import settings
from pyblog.urls import urls


define("port", default=8000, help="run on the given port", type=int)

def main():
    tornado.options.parse_command_line()

    handlers = []
    for handler in urls:
        handlers.extend(handler)

    app = tornado.web.Application( handlers=handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()

if __name__ == '__main__':
    main()
