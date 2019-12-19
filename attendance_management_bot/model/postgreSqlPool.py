#!/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2020-present Works Mobile Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
Connection pool for database

    reference
    - https://cito.github.io/DBUtils/UsersGuide.html#pooleddb
"""

import psycopg2
import psycopg2.extras as extras
from psycopg2.errors import DuplicateTable
from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB
from attendance_management_bot.constant import DB_CONFIG


class PostGreSql:
    __pool = None
    _conn = None
    _cursor = None

    def __init__(self):
        return

    def cursor(self):
        self._conn = PostGreSql.__get_conn()
        self._cursor = self._conn.cursor()
        return self._cursor

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def execute(self, sql):
        self._cursor.execute(sql)

    def fetchall(self):
        return self._cursor.fetchall()

    def fetchone(self):
        return self._cursor.fetchone()

    def close(self):
        self._conn.close()
        self._cursor.close()

    def __enter__(self):
        return self.cursor()

    def __exit__(self, type, value, tb):
        if tb is None:
            self.commit()
        else:
            self.rollback()
        self.close()

    @staticmethod
    def __get_conn():
        if PostGreSql.__pool is None:
            __pool = PooledDB(creator=psycopg2, mincached=1, maxcached=20,
                              host=DB_CONFIG["host"],
                              port=DB_CONFIG["port"],
                              user=DB_CONFIG["user"],
                              password=DB_CONFIG["password"],
                              database=DB_CONFIG["dbname"],
                              sslmode=DB_CONFIG["sslmode"])
        return __pool.connection()
