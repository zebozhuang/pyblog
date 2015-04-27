# utf-8

import time

import init_path
import unittest
from pyblog.libs.sqlpool import SqlPool
from pyblog.settings import MYSQL_DATABASE as db


class SqlPoolTest(unittest.TestCase):
    def setUp(self):
        self.pool = SqlPool(host=db['host'],
            user=db['user'],
            passwd=db['passwd'],
            db='pyblog_test') 
        self.create_table = 'create table if not exists foo(a int);'

    def test_execute(self):
        print self.pool.execute(self.create_table)

    def test_insert(self):
        sql = "insert into foo(a) values(%d);" % int(time.time())
        print self.pool.execute(sql)

    def test_query(self):
        sql = "select * from foo;"
        print self.pool.query(sql)

if __name__ == '__main__':
    unittest.main()
