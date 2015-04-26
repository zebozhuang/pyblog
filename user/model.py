#!/usr/bin/env python
# -*- coding: utf-8 -*-


class User(object):
    TABLE = 'user'
    STRUCT = "create table `%s`(
        uid    UNSIGNED INT NOT NULL AUTO_INCREMENT,
        name   VARCHAR(30) NOT NULL DEFAULT '',
        email  VARCHAR(30) NOT NULL,
        passwd BINARYCHAR(20) NOT NULL DEFAULT '',
        sex    ENUM('male', 'femail'),
        KEY    email_key (email),
    ) ENGINE=innodb DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"

