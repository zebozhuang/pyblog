#!/usr/bin/env python
#-*- coding: utf-8 -8-

import tornado.web

class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
