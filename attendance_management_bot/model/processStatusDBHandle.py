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
bot_process_status table's CRUD operation.
save the user context.
Check also: scripts/initDB.py
"""

__all__ = ['insert_replace_status_by_user_date', 'set_status_by_user_date',
           'get_status_by_user', 'delete_status_by_user_date',
           'clean_status_by_user']

import logging
from attendance_management_bot.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable, DuplicateObject

LOGGER = logging.getLogger("attendance_management_bot")


def insert_replace_status_by_user_date(account, date, status, process=None):
    """
    insert or update user's status.

    :param account: user account
    :param date: current date by local time.
    :param status: user text input status.
    :param process: processing progress.
    :return: Return false when status is None Else, Return None
    """

    if status is None:
        return False

    insert_sql = "INSERT INTO bot_process_status(account, cur_date, status)" \
                 " VALUES('%s', '%s', '%s') ON CONFLICT(account, cur_date) " \
                 "DO UPDATE SET status='%s', update_time=now()" % \
                 (account, date, status, status)
    if process is not None:
        insert_sql = "INSERT INTO bot_process_status(" \
                     "account, cur_date, status, process) " \
                     "VALUES('%s', '%s', '%s', '%s') " \
                     "ON CONFLICT(account, cur_date) " \
                     "DO UPDATE SET " \
                     "status='%s', process='%s', update_time=now()" % \
                     (account, date, status, process, status, process)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(insert_sql)


def set_status_by_user_date(account, date, status=None, process=None):
    """
    update user's status.

    :param account: user account
    :param date: current date by local time.
    :param status: user text input status.
    :param process: processing progress.
    :return: no
    """

    condition = "WHERE account='%s' and cur_date='%s'" % (account, date)

    update_sql = "UPDATE bot_process_status SET update_time=now()"
    if status is not None:
        update_sql = "%s , status='%s'" % (update_sql, status,)
    if process is not None:
        update_sql = "%s , process='%s'" % (update_sql, process,)

    update_sql = "%s %s" % (update_sql, condition,)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(update_sql)


def get_status_by_user(account, date):
    """
    select user's status.

    :param account: user account
    :param date: current date by local time.
    :return: no
    """

    select_sql = "SELECT status, process " \
                 "FROM bot_process_status " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    row = None
    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        if rows is not None and len(rows) == 1:
            # ['status', 'process']
            row = rows[0]
    return row


def delete_status_by_user_date(account, date):
    """
    delete user's status.

    :param account: user account
    :param date: current date by local time.
    :return: no
    """

    delete_status_sql = "UPDATE bot_process_status SET status=NULL, " \
                        "update_time=now() " \
                        "WHERE account='%s' and cur_date='%s'" % \
                        (account, date)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(delete_status_sql)


def clean_status_by_user(account, date):
    """
    delete a item.

    :param account: user account
    :param date: current date by local time.
    :return: no
    """

    delete_sql = "DELETE FROM bot_process_status " \
                 "WHERE account='%s' and cur_date='%s' " % (account, date)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(delete_sql)
