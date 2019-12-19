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
bot_calendar_record table's CRUD operation.
This table is used to save the time of the user.
Check also: scripts/initDB.py
"""

__all__ = ['set_schedule_by_user', 'get_schedule_by_user',
           'modify_schedule_by_user', 'clean_schedule_by_user']

import logging
from attendance_management_bot.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable

LOGGER = logging.getLogger("attendance_management_bot")


def set_schedule_by_user(schedule_id, account, date,  begin, end):
    """
    insert schedule

    :param schedule_id: schedule_id
    :param account: user account
    :param date: current date by local time.
    :param begin: schedule begin time.
    :param end: schedule end time.
    :return: no
    """

    insert_sql = "INSERT INTO bot_calendar_record(schedule_id, account, " \
                 "cur_date, begin_time, end_time) " \
                 "VALUES('%s', '%s', '%s', %d, %d)" \
                 % (schedule_id, account, date, begin, end)

    post_gre = PostGreSql()

    with post_gre as cursor:
        cursor.execute(insert_sql)


def get_schedule_by_user(account, date):
    """
    get schedule

    :param account: user account
    :param date: current date by local time.
    :return: schedule id, begin time
    """
    select_sql = "SELECT schedule_id, begin_time " \
                 "FROM bot_calendar_record " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    row = None
    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        if rows is not None and len(rows) == 1:
            # ["schedule_id", "begin_time"]
            row = rows[0]
    return row


def modify_schedule_by_user(schedule_id, end):
    """
    update schedule's end time

    :param schedule_id: schedule_id
    :param end: schedule end time.
    :return: no
    """
    select_sql = "UPDATE bot_calendar_record " \
                 "SET end_time=%d, update_time=now()" \
                 "WHERE schedule_id='%s'" \
                 % (end, schedule_id)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)


def clean_schedule_by_user(account, date):
    """
    delete a schedule

    :param account: user account
    :param date: current date by local time.
    :return: no
    """
    delete_sql = "DELETE FROM bot_calendar_record " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(delete_sql)
