# !/bin/env python
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
Handle the user's direct check-in
"""

__all__ = ['deal_sign_in_message', 'direct_sign_in']

import tornado.web
import asyncio
import logging
from attendance_management_bot.model.data import make_quick_reply
from attendance_management_bot.model.i18n_data import make_i18n_text
from attendance_management_bot.externals.send_message import push_message
from attendance_management_bot.actions.message import invalid_message, TimeStruct, \
    create_quick_replay_items
from attendance_management_bot.model.processStatusDBHandle \
    import get_status_by_user, delete_status_by_user_date
import gettext
_ = gettext.gettext

LOGGER = logging.getLogger("attendance_management_bot")


def deal_sign_in_message(sign_time, manual_flag):
    """
    Generate a message returned to the user when checking in.

    :param sign_time: The user's check-in time is a timestamp.
    :param manual_flag: Boolean value. True is manually enters time.
    :return: message content is a json.
    """
    call_back = "sign_in"
    if manual_flag:
        call_back = "manual_sign_in"

    user_time = TimeStruct(sign_time)

    fmt = _("Register the current time {date} as clock-in time?")
    fmt1 = _("%A, %B %-d at %-I:%M %P")

    text = make_i18n_text("Register the current time {date} as clock-in time?",
                          "direct_sign_in", fmt, fmt1=fmt1,
                          date=user_time.date_time)

    if manual_flag:
        fmt = _("Register the entered {date} as clock-in time?")
        text = make_i18n_text("Register the entered {date} as clock-in time?",
                              "direct_sign_in", fmt, fmt1=fmt1,
                              date=user_time.date_time)

    reply_items = create_quick_replay_items(
        "confirm_in&time=" + user_time.str_current_time_tick, call_back)

    text["quickReply"] = make_quick_reply(reply_items)

    return text


@tornado.gen.coroutine
def deal_sign_in(account_id, current_date, sign_time, manual_flag=False):
    content = get_status_by_user(account_id, current_date)

    if content is not None:
        status = content[0]
        process = content[1]
        if process is not None:
            return invalid_message()

        if status == "wait_in" or status == "in_done":
            delete_status_by_user_date(account_id, current_date)

    return deal_sign_in_message(sign_time, manual_flag)


@tornado.gen.coroutine
def direct_sign_in(account_id, current_date, sign_time, _):
    """
    Handle the user's direct check-in.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param sign_time: Time when the user clicks to check-in.
    :param _: no use
    """
    content = yield deal_sign_in(account_id, current_date, sign_time)

    yield push_message(account_id, content)
