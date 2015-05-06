#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append("..")

def include(module):
    __import__(module)
    return getattr(sys.modules[module], 'urls')


urls = [
    include("pyblog.login.urls"),                
    include("pyblog.home.urls"),                
]
