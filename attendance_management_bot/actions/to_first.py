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

import tornado.web
import logging
from attendance_management_bot.model.i18n_data import make_i18n_text
from attendance_management_bot.externals.send_message import push_message
import gettext
_ = gettext.gettext

LOGGER = logging.getLogger("attendance_management_bot")


@tornado.gen.coroutine
def to_first(account_id, ____, __, ___):
    fmt = _("Please select \"Record\" on the bottom of "
            "the menu each time when you clock in and clock out.")
    content = make_i18n_text("Please select \"Record\" on the bottom of the "
                             "menu each time when you clock in and clock out.",
                             "to_first", fmt)
    yield push_message(account_id, content)
