# utf-8

import init_path
import unittest
from pyblog.libs.sqlpool import SqlPool
from pyblog.settings import MYSQL_DATABASE as db


class SqlPoolTest(unittest.TestCase):
    def Setup(self):
        self.pool = SqlPool(host=db['host'],
            user=db['user'],
            passwd=db['passwd'],
            db='pyblog_test') 

    def TearDown(self):
        pass
