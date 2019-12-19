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
deal user input messages
"""

__all__ = ['deal_user_message', 'deal_message']

import tornado.web
import time
import logging
from tornado.web import HTTPError
from attendance_management_bot.common.local_timezone import local_date_time
from attendance_management_bot.externals.send_message import push_messages
from attendance_management_bot.actions.message import invalid_message, error_message
from attendance_management_bot.actions.direct_sign_in import deal_sign_in
from attendance_management_bot.actions.direct_sign_out import deal_sign_out
from attendance_management_bot.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date

LOGGER = logging.getLogger("attendance_management_bot")


@tornado.gen.coroutine
def deal_user_message(account_id, current_date, create_time, message):
    """
    Process messages entered by users,
    Different scenarios need different processing functions.
    Please see the internal implementation of the handler.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param create_time: Time when the user requests to arrive at the BOT server.
    :param message: User entered message.
    :return: message content
    """

    date_time = local_date_time(create_time)

    content = get_status_by_user(account_id, current_date)

    if content is None or content[0] is None:
        LOGGER.info("status is None account_id:%s message:%s content:%s",
                    account_id, message, str(content))
        raise HTTPError(403, "Messages not need to be processed")

    status = content[0]
    process = content[1]
    try:
        user_time = int(message)
    except Exception:
        if status == "wait_in" or status == "wait_out":
            return error_message()
        else:
            raise HTTPError(403, "Messages not need to be processed")

    if len(message) != 4:
        return error_message()

    hour = int(user_time / 100)
    minute = int(user_time % 100)
    if (status == "wait_in" or status == "wait_out") \
            and ((hour < 0 or hour > 23) or (minute < 0 or minute > 59)):
        return error_message()

    tm = date_time.replace(hour=hour, minute=minute)
    user_time_ticket = int(tm.timestamp())

    if status == "wait_in":
        content = yield deal_sign_in(account_id,
                                     current_date, user_time_ticket, True)
        set_status_by_user_date(account_id, current_date, status="in_done")
        return [content]
    if status == "wait_out":
        content, status = yield deal_sign_out(account_id,
                                      current_date, user_time_ticket, True)
        if status:
            set_status_by_user_date(account_id, current_date, status="out_done")

        return content
    if process == "sign_in_done" or process == "sign_out_done":
        return [invalid_message()]

    LOGGER.info("can't deal this message account_id:%s message:%s status:%s",
                account_id, message, status)
    raise HTTPError(403, "Messages not need to be processed")


@tornado.gen.coroutine
def deal_message(account_id, current_date, create_time, message):
    """
    Process messages manually entered by the user.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param create_time: Time the request arrived at the server.
    :param callback: User triggered callback.
    :return: None
    """

    contents = yield deal_user_message(account_id, current_date,
                                       create_time, message)

    yield push_messages(account_id, contents)
