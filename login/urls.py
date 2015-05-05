#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyblog.login.views import LoginHandler, RegisterHandler


urls = [
    ("/login/?", LoginHandler),       
    ("/register/?", RegisterHandler),
]
