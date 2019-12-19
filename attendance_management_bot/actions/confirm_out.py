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
Deal confirm check-out
"""

__all__ = ['confirm_out']

import tornado.gen
import asyncio
import time
import locale
import logging
from datetime import datetime
from tornado.web import HTTPError
from attendance_management_bot.common import global_data
from attendance_management_bot.common.local_timezone import local_date_time
from attendance_management_bot.model.data import i18n_text, make_text
from attendance_management_bot.model.i18n_data import \
    make_i18n_text, get_i18n_content_by_lang, get_i18n_content
from attendance_management_bot.externals.calendar_req import modify_schedule
from attendance_management_bot.externals.send_message import push_messages
from attendance_management_bot.actions.message import invalid_message, prompt_input, \
    TimeStruct, number_message
from attendance_management_bot.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date
from attendance_management_bot.model.calendarDBHandle import get_schedule_by_user, \
    modify_schedule_by_user
from attendance_management_bot.common.contacts import get_user_info_by_account
from conf.config import DEFAULT_LANG
import gettext
_ = gettext.gettext

LOGGER = logging.getLogger("attendance_management_bot")


def confirm_out_message(user_time, total_hours, total_minutes):
    date_time = local_date_time(user_time)

    fmt = _(" ")
    str_hours = ""
    hours_content = get_i18n_content(fmt, "confirm_out")

    if total_hours != 0:
        str_hours = "{total_hours} hours and "
        fmt = _("{total_hours} hours and ")
        hours_content = get_i18n_content(fmt, "confirm_out")
        for key in hours_content:
            hours_content[key] = hours_content[key].format(
                total_hours=total_hours)

    fmt1 = _(
        "Clock-out time has been registered. "
        "The total working hours for {date} is {total_hours}{total_minutes} minutes.")
    texts = get_i18n_content(fmt1, "confirm_out")

    fmt2 = _("%A, %B %d")
    dates = get_i18n_content(fmt2, "confirm_out")

    i18n_texts = []
    for key in texts:
        locale.setlocale(locale.LC_TIME,
                         "{lang}{code}".format(lang=key, code=".utf8"))
        value = texts[key].format(date=date_time.strftime(dates[key]),
                                  total_hours=hours_content[key],
                                  total_minutes=total_minutes)
        i18n_texts.append(i18n_text(key, value))

    locale.setlocale(locale.LC_TIME,
                     "{lang}{code}".format(lang="en_US", code=".utf8"))
    return make_text("Clock-out time has been registered. "
                     "The total working hours for {date} "
                     "is{total_hours}{total_minutes} minutes."
                     .format(date=date_time.strftime('%A, %B %d'),
                             total_hours=str_hours,
                             total_minutes=total_minutes),
                     i18n_texts=i18n_texts)


@tornado.gen.coroutine
def deal_confirm_out(account_id, create_time, callback):
    """
    will be linked with the calendar internally, Check out time of registered user.
    Check also: attendance_management_bot/externals/calendar_req.py

    :param account_id: user account id.
    :param create_time: current date by local time.
    :param callback: The message content of the callback,
        include the user's check-out time
    :return: Prompt message of successful check out.
    """
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    user_time = int(str_time)

    end_time = local_date_time(user_time)
    current_date = datetime.strftime(end_time, '%Y-%m-%d')

    info = get_schedule_by_user(account_id, current_date)
    if info is None:
        raise HTTPError(500, "Internal data error")
    schedule_id = info[0]
    begin_time_st = info[1]

    cur_time = local_date_time(create_time)
    begin_time = local_date_time(begin_time_st)

    fmt = _("{account}'s working hours on {date}")
    fmt1 = _("%A, %B %d")
    title = get_i18n_content_by_lang(fmt, "confirm_out", DEFAULT_LANG, fmt1=fmt1,
                                     account=get_user_info_by_account(
                                         account_id), date=end_time)
    modify_schedule(schedule_id, cur_time, end_time, begin_time,
                    account_id, title)

    modify_schedule_by_user(schedule_id, user_time)

    hours = int((user_time - begin_time_st)/3600)
    min = int(((user_time - begin_time_st) % 3600)/60)

    return [confirm_out_message(user_time, hours, min)]


@tornado.gen.coroutine
def confirm_out(account_id, current_date, create_time, callback):
    """
    This function is triggered when the user clicks confirm check-out.
    will be linked with the calendar internally.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param create_time: Time the request arrived at the server.
    :param callback: User triggered callback.
    :return: None
    """
    contents = yield deal_confirm_out(account_id, create_time, callback)

    set_status_by_user_date(account_id, current_date,
                            status="out_done", process="sign_out_done")
    yield push_messages(account_id, contents)
