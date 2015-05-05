#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pyblog.user import userManager


def getUser(userid):
    user = userManager.get(userid)
    return user


def addUser(name, email, passwd, sex):
    user = userManager.create(name, email, passwd, sex)
    return user


