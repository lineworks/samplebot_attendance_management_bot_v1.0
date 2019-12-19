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
common message
"""

__all__ = ['TimeStruct', '__init__', 'create_button_actions',
           'create_quick_replay_items', 'prompt_input', 'number_message',
           'error_message', 'invalid_message', 'reminder_message']

import time
import logging
from attendance_management_bot.model.data import make_quick_reply_item
from attendance_management_bot.model.i18n_data import make_i18n_message_action, \
    make_i18n_postback_action, make_i18n_text
from attendance_management_bot.constant import API_BO, IMAGE_CAROUSEL, RICH_MENUS
from attendance_management_bot.common.local_timezone import local_date_time
import gettext
_ = gettext.gettext

LOGGER = logging.getLogger("attendance_management_bot")


class TimeStruct:
    """
    to localize timestamp time
    """

    def __init__(self, sign_time):
        """
        Convert timestamp time to datetime time in a specific time zone.
        And assign it to the corresponding member variable.

        :param sign_time: A user time of timestamp value.
        """

        self.date_time = local_date_time(sign_time)
        self.str_current_time_tick = str(sign_time)
        pos = self.str_current_time_tick.find(".")
        if pos != -1:
            self.str_current_time_tick = self.str_current_time_tick[:pos]


def create_button_actions(direct_sign_callback, manual_sign_callback):
    """
    Create the message body of the button template of two buttons.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/100500804?lang=en

    :param direct_sign_callback: callback string for the first button.
    :param manual_sign_callback: callback string for the seconds button.
    """
    fmt1 = _("Current time")
    fmt2 = _("Manually enter")
    action1 = make_i18n_message_action(direct_sign_callback,
                                       "message", "Current time", fmt1)
    action2 = make_i18n_message_action(manual_sign_callback,
                                       "message", "Manually enter", fmt2)

    return [action1, action2]


def create_quick_replay_items(confirm_callback, previous_callback):
    """
    Building a quick reply floating window for messages.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/100500807?lang=en

    :param confirm_callback: callback string for the first button.
    :param previous_callback: callback string for the seconds button.
    :return: quick replay items
    """
    fmt1 = _("Yes")
    action1 = make_i18n_postback_action(confirm_callback, "message",
                                        "Yes", fmt1, "Yes", fmt1)
    reply_item1 = make_quick_reply_item(action1)

    fmt2 = _("No")
    action2 = make_i18n_postback_action(previous_callback, "message",
                                   "No", fmt2, "No", fmt2)
    reply_item2 = make_quick_reply_item(action2)

    return [reply_item1, reply_item2]


def prompt_input():
    """
    Format to remind users to enter time.

    :return: text type message
    """

    fmt = _("Please use the military time format with a total of 4 numerical "
            "digits (hhmm) when entering the time. "
            "For example, type 2020 to indicate 8:20 PM. ")

    return make_i18n_text("Please use the military time format "
                          "with a total of 4 numerical digits (hhmm) "
                          "when entering the time. For example, "
                          "type 2020 to indicate 8:20 PM. ",
                          "message", fmt)


def number_message():
    """
    Non digital message entered.

    :return: text type message
    """
    fmt = _("Clock-out time was recorded as being earlier than the time of "
            "clock-in. Please check the clock-out time again and re-enter it. ")
    text1 = make_i18n_text("Clock-out time was recorded as being earlier "
                           "than the time of clock-in."
                           "Please check the clock-out time again "
                           "and re-enter it. ",
                           "message", fmt)

    text2 = prompt_input()
    return [text1, text2]


def error_message():
    """
    Wrong data entered

    :return: text type message
    """
    fmt = _("Sorry, but unable to comprehend your composed time. "
            "Please check the time entry method again, and enter the time.")
    text1 = make_i18n_text("Sorry, but unable to comprehend your composed time. "
                           "Please check the time entry method again, "
                           "and enter the time.", "message", fmt)

    text2 = prompt_input()
    return [text1, text2]


def invalid_message():
    """
    Invalid input data reminder.

    :return: text type message
    """
    fmt = _("The text could not be understood. "
            "Please select the appropriate \"Record\" button on "
            "the bottom of the menu when you clock in or clock out.")

    return make_i18n_text("The text could not be understood. "
                          "Please select the appropriate \"Record\" button on "
                          "the bottom of the menu when you clock in or clock out.",
                          "message", fmt)


def reminder_message(process):
    """
    Illegal request reminder.

    :param process: Current user's progress
    :return: text type message
    """
    text = None
    if process == "sign_in_done":
        fmt = _("There is already a clock-in time. Please select "
                "\"Record\" on the bottom of the menu when you clock out.")
        text = make_i18n_text("There is already a clock-in time. "
                              "Please select \"Record\" on the "
                              "bottom of the menu when you clock out.",
                              "message", fmt)

    elif process == "sign_out_done":
        fmt = _("There is already a clock-out time. "
                "Please select \"Record\" on the bottom "
                "of the menu when you clock in.")
        text = make_i18n_text("There is already a clock-out time. "
                              "Please select \"Record\" on the bottom "
                              "of the menu when you clock in.",
                              "message", fmt)
    elif process is None:
        fmt = _("Today's clock-in time has not been registered. "
                "Please select \"Record clock-in\" on the bottom of the menu, "
                "and enter your clock-in time.")
        text = make_i18n_text("Today's clock-in time has not been registered. "
                              "Please select \"Record clock-in\" on the bottom "
                              "of the menu, and enter your clock-in time.",
                              "message", fmt)
    return text
