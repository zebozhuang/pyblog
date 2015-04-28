#!/usr/bin/env python
# -*- coding: utf-8 -*-

import init_path

import time
import unittest

from pyblog.user import userManager


class UserManagerTest(unittest.TestCase):
    def test_create(self):
        name = "foo" 
        email = "foo_%d@example.com" % int(time.time())
        passwd = "foo"
        sex = "male"

        assert userManager.create(name, email, passwd, sex)

    def test_get(self):
        pass


if __name__ == "__main__":
    unittest.main()
    
