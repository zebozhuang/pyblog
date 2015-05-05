#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyblog.libs.sqlpool import SqlPool 
from pyblog.libs.utils import mysql_escape 

from pyblog.settings import MYSQL_DATABASE as db

from model import User

class UserManager(object):
    def __init__(self, table, struct):
        self.table = table
        self.pool = SqlPool(db['host'], db['user'], db['passwd'], db['db'])
        self.pool.execute(struct) 

    def create(self, name, email, passwd, sex):
        """create user"""
        # encrypt passwd
        sql = ("INSERT INTO`%s`(name,email,passwd,sex) " 
               "VALUES('%s', '%s', '%s', '%s');") % (self.table, mysql_escape(name),
               mysql_escape(email), mysql_escape(passwd), mysql_escape(sex))

        affected_rows, insertid  = self.pool.execute_return_insertid(sql)

        if affected_rows <=0:
            return {}

        user = {'uid': insertid, 'name': name, 'email': email, 'sex': sex}
        return self._format(user)

    def get(self, uid):
        """get user by uid"""
        sql = ("SELECT uid, name, email, sex FROM `%s`;") % self.table

        user = self.pool.query(sql, 2)
        return self._format(user)

    def _format(self, user):
        """format user infomation"""
        if not user:
            return {}

        user['uid'] = int(user['uid'])
        user['name'] = str(user['name'])
        user['email'] = str(user['email'])
        user['sex'] = str(user['sex'])
        return user
    
