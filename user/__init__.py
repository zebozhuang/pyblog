#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pyblog.user.model import User 
from pyblog.user.view import UserManager

userManager = UserManager(User.TABLE, User.STRUCT)
