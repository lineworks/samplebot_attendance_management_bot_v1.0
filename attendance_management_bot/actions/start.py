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
Start using robots
"""

__all__ = ['image_introduce', 'sign', 'start']

import tornado.web
import logging
from attendance_management_bot.model.data import make_image_carousel
from attendance_management_bot.model.i18n_data \
    import make_il8n_image_carousel_column, make_i18n_postback_action, \
    make_i18n_text
from attendance_management_bot.constant import RICH_MENUS, \
    IMAGE_CAROUSEL
from conf.config import DEFAULT_LANG
from attendance_management_bot.externals.send_message import push_messages
from attendance_management_bot.common.global_data import get_value
from attendance_management_bot.externals.richmenu \
    import set_user_specific_rich_menu
import gettext
_ = gettext.gettext

LOGGER = logging.getLogger("attendance_management_bot")


def image_introduce():
    """
    This function constructs three image carousels for self introduction.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/100500809?lang=en

    :return: image carousels type message content.
    """

    fmt = _("Try now")
    action1 = make_i18n_postback_action("a", "start", "Try now", fmt)
    column1 = make_il8n_image_carousel_column(0, action=action1)

    action2 = make_i18n_postback_action("b", "start", "Try now", fmt)
    column2 = make_il8n_image_carousel_column(1, action=action2)

    action3 = make_i18n_postback_action("c", "start", "Try now", fmt)

    column3 = make_il8n_image_carousel_column(2, action=action3)

    columns = [column1, column2, column3]
    return make_image_carousel(columns)


@tornado.gen.coroutine
def sign(account_id):
    """
    Set up rich menu for chat with users.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/1005040?lang=en

    :param account_id: user account id
    """
    if account_id is None:
        LOGGER.error("account_id is None.")
        return False
    rich_menu_id = get_value(DEFAULT_LANG, None)
    if rich_menu_id is None:
        LOGGER.error("get rich_menu_id failed.")
        raise Exception("get rich_menu_id failed.")

    return set_user_specific_rich_menu(rich_menu_id, account_id)


@tornado.gen.coroutine
def start_content(account_id):
    yield sign(account_id)

    fmt = _("Hello, I'm an attendance management bot of WORKS "
            "that helps your timeclock management and entry.")
    content1 = make_i18n_text("Hello, I'm an attendance management bot of "
                         "WORKS that helps your timeclock "
                         "management and entry.", "start", fmt)
    content2 = image_introduce()

    return [content1, content2]


@tornado.gen.coroutine
def start(account_id, _, __, ___):
    """
    Handle the user start using robots.
    Send the robot's self introduction information,
    and the chat room is bound with rich menu.

    :param account_id: user account id.
    """
    contents = yield start_content(account_id)

    yield push_messages(account_id, contents)
