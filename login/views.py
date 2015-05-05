#/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("register")


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("[get] login")

    def post(self):
        self.write("login")
