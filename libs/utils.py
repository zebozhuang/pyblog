#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _mysql


def mysql_escape(args):
    if args is None:
        return ''
    if isinstance(args, unicode):
        args = args.encode('utf8')
    if not isinstance(args, str):
        args = str(args)
    return _mysql.escape_string(args)

