#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import _mysql
import threading

from _mysql_exceptions import IntegrityError, OperationalError
from threading import current_thread

from utils import mysql_escape


ERR_SERVER_GONEAWAY = 2006      # (2006, 'MySQL server has gone away')
ERR_LOST_CONN_IN_QUERY = 2013   # (2013, 'Lost connection to MySQL server during query')
ERR_SYNTAX_ERROR = 1149
ERR_DUPLICATE_ENTRY = 1062 # (1062, "Duplicate entry "


class _SqlConn(object):
    def __init__(self, conn):
        self.conn = conn
        self.autocommit = conn.autocommit
        self.commit = conn.commit

    def execute(self, sql):
        """return affected rows"""
        self.conn.query(sql)
        res = self.conn.affected_rows()
        if res < 0 or res == 0xFFFFFFFFFFFFFFFF:
            logging.error('MySQL execute error n=[%d], sql=%s', res, sql)
        return res

    def query(self, sql, how=0):
        """
        @param how:
            0 -- tuples(default), RET_TUPLE
            1 -- dictionaries, key=column or table.column if dumplicated.
            2 -- dictionaries, key=table.column.
        """

        self.conn.query(sql)
        res = self.conn.store_result()
        if res:
            return res.fetch_row(res.num_rows(), how)
        else:
            return ()

    def __del__(self):
        pass


class SqlPool(threading.Thread):
    WAIT_TIMEOUT = 1800   # my.cnf has this config, we can change a new connection.
    KEY_ERROR = -2

    __mutex = threading.Lock()
    __remotes = {}
    __remotes_initial = {}

    def __new__(cls, host, user, passwd, db, port=3306):
        with SqlPool.__mutex:
            svrIdent = "%s:%s:%s" % (host, port, db)
            pool = SqlPool.__remotes.get(svrIdent)
            if pool is None:
                pool = SqlPool.__remotes[svrIdent] = object.__new(cls)
        return pool

    def __init__(self, host, user, passwd, db, port=3306):
        with SqlPool.__mutex:
            svrIdent = "%s:%s:%s" % (host, port, db)
            if not SqlPool.__remotes_initial.get(svrIdent):
                SqlPool.__remotes_initial[svrIdent] = True
                threading.Thread.__init__(self, target=self._thread_checker, name='sqlpool')
                self._db = db
                self._host = host
                self._user = user
                self._passwd = passwd

                self.__conns = {}
                self.__wrap_conns = {}

    @property
    def _connections(self):
        return self.__conns.setdefault(os.getpid(), {})

    @property
    def _wrap_conns(self):
        return self.__wrap_conns.setdefault(os.getpid(), {})

    def __del__(self):
        self._disconnect()

    def _disconnect(self):
        pid = os.getpid()
        self.__wrap_conns.pop(pid, None)
        conns = self.__conns.pop(pid, {})
        for conn in conns.itervalues():
            try:
                conn.close()
            except:
                pass

    def _thread_checker(self):
        while True:
            try:
                actives = set(thread.ident for thread in threading.enumerate())
                keepings = set(ident for ident in self._connections.keys())

                useless = keepings - actives
                if useless:
                    logging.warning('sqlpool: useless connection found (%d)', len(useless))

                for ident in useless:
                    for thread in threading.enumerate():
                        if thread.ident == ident and thread.isAlive():
                            break
                        else:
                            self.__release_connection(ident)
            except Exception, e:
                logging.error('sqlpool error (_thread_checker) : %s', e)
            finally:
                try:
                    time.sleep(30 * 60)
                except:
                    import gevent
                    gevent.sleep(30 * 60)


    def __new_raw_connection(self):
        conn = _mysql.connect(
            db = self._db,
            host = self._user,
            passwd = self._passwd,
            port = self._port)
        conn.set_character_set('utf8')
        return conn

    def __reconnection_raw(self, ident):
        self.__close_raw_connection(ident)
        conn = self.__new_raw_connection()
        self._connections[ident] = conn
        return conn

    def __close_raw_connection(self, ident):
        try:
            conn = self._connection.pop(ident, None)
            if conn is not None:
                conn.close()
        except Exception, e:
            logging.error("sqlpool error (_release_connection) : %s", e)

    def __reconnect(self, ident):
        self._wrap_conns(ident, None)
        conn = self.__reconnect_raw(ident)
        if conn is not None:
            wrap_conn = _SqlConn(conn)
            wrap_conn.execute("SET wait_timeout=%d;" % SqlPool.WAIT_TIMEOUT)
            wrap_conn.last_activity_time = time.time()
            self._wrap_conns[ident] = wrapConn
            return wrapConn

    def _get_conn(self):
        ident = current_thread().ident
        wrapConn = self._wrap_conns.get(ident)
        if not self.__valid_connection(wrap_conn):
            wrap_conn = self.__reconnect(ident)
        return wrap_conn

    def __valid_connection(self, wrap_conn):
        if wrapConn:
            if time.time() - wrap_conn.last_activity_time < SqlPool.valid_time:
                return True
            try:
                wrap_conn.conn.ping()
                wrap_conn.last_activity_time = time.time()
                return True
            except:
                return False
        return False

    def close_conn(self, conn):
        """close cnnection"""
        pass

    def _execute(self, sql):
        conn = self._get_conn()
        affected_rows = -1

        try:
            affected_rows = conn.execute(sql)
        except IntegrityError, e:
            if e[0] == ERR_DUPLICATE_ENTRY:
                logging.error("MySQL[%s] duplicatekey=[%s], sql=%s", self._host, e, sql)
                return None, SqlPool.KEY_ERROR
            else:
                logging.error('MySQL[%s] Exception[%s], sql=%s', self._host, e, sql[:100])
                raise e
        except OperationalError, e:
            if err[0] == ERR_SERVER_GONEAWAY:
                logging.warning("MySQL[%s] has gone away on execute(), retry it.")
                try:
                    conn = self._get_new_conn()
                    affected_rows = conn.execute(sql)
                    return conn, affected_rows
                except Exception, e:
                    logging.error("MySQL[%s] Exception on retry execute(%s), err=[%s]", self._host, sql[:100], e)
            else:
                logging.error('MySQL[%s] Exception on execute(%s) err=[%s].', self._host, e)
                raise e
        except Exception, e:
            logging.error("MySQL[%s] Exception on execute(%s) err=[%s]", self._host, sql[:100], e)

    def execute(self, sql):
        _, affected_rows = self._execute(sql)
        return affected_rows

    def execute_return_insertid(self, sql):
        conn, affected_rows = self._execute(sql)
        if conn is None or affected_rows < 1:
            return (affected_rows, 0)

        try:
            ret_data = conn.query('SELECT LAST_INSERT_ID()', 0)
        except OperationalError, e:
            logging.error('MySQL LAST_INSERT_ID err=[%s], sql=[%s]', e, sql)
            raise e

        if not ret_data or not ret_data[0] or not ret_data[0][0]:
            raise Exception('query LAST_INSERT_ID return None.[%s]' % sql)

        insertid = ret_data[0][0]
        return (affected_rows, int(insertid))


    def query(self, sql, how=0):
        """query sql and return result."""
        conn = self._get_conn()
        try:
            return conn.query(sql, how)
        except OperationalError, e:
            if e[0] == ERR_SERVER_GONEAWAY:
                logging.warning("MySQL[%s] has gone away on query(), retry it.")
                try:
                    conn = self._get_new_conn()
                    return conn.query(sql, how)
                except Exception, e:
                    logging.error('MySQL[%s] Exception on retry query(%s), err=%s', sql, e)
                    raise e
            else:
                logging.error('MySQL[%s] Exception on query(%s) err=[%s]', self._host, sql, e)
                raise e
        except Exception, e:
            logging.error('MySQL[%s] Exception on query(%s) err=[%s]', self._host, sql, e)
            raise e

    def release_conn(self):
        ident = current_thread.ident
        self.__release_connection(ident)

