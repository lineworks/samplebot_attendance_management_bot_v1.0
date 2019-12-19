#!/bin/env python3
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
the url to handler route
"""

__all__ = ['getRouter']

import tornado.web
from attendance_management_bot.callbackHandler import CallbackHandler
from attendance_management_bot.constant import FILE_SYSTEM


def getRouter():
    """
    get the app with route info

        reference
        - https://www.tornadoweb.org/en/stable/web.html

    StaticFileHandler is a simple handler that can serve static content
    from a directory.

        reference
        - https://www.tornadoweb.org/en/stable/web.html#tornado.web.StaticFileHandler
    """

    return tornado.web.Application([
        (r"/callback", CallbackHandler),
        (r'/static/([a-zA-Z0-9\&%_\./-~-]*.([p|P][n|N][g|G]))',
            tornado.web.StaticFileHandler, 
            {"path": FILE_SYSTEM["image_dir"]}),
    ])
