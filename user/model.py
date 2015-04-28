#!/usr/bin/env python
# -*- coding: utf-8 -*-


class User(object):
    TABLE = 'user'
    STRUCT = """CREATE TABLE IF NOT EXISTS`%s`(
        uid    INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
        name   VARCHAR(30) NOT NULL DEFAULT '',
        email  VARCHAR(30) NOT NULL,
        passwd VARBINARY(20) NOT NULL DEFAULT '',
        sex    ENUM('male','female') NOT NULL,
        UNIQUE KEY _email (email),
        PRIMARY KEY _uid (uid)
    ) ENGINE=InnoDB AUTO_INCREMENT=20150428 DEFAULT CHARSET=utf8;""" % TABLE

