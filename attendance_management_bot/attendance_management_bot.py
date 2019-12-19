#!/bin/bash python
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
launch attendance_management_bot
"""

__all__ = ['sig_handler', 'kill_server', 'init_logger', 'check_init_bot',
           'init_rich_menu_first', 'init_calendar_first',
           'start_attendance_management_bot']

import os
import logging
from logging import StreamHandler
import asyncio
import uvloop
import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options
from attendance_management_bot.externals.richmenu import init_rich_menu
from conf.config import DEFAULT_LANG
from attendance_management_bot.common import global_data
from attendance_management_bot.externals.calendar_req import init_calendar
from attendance_management_bot.constant import API_BO, RICH_MENUS
from attendance_management_bot.model.initStatusDBHandle import insert_init_status, \
    get_init_status

import psutil

import attendance_management_bot.router
import attendance_management_bot.contextlog
from attendance_management_bot.settings import CALENDAR_PORT, CALENDAR_LOG_FMT, \
    CALENDAR_LOG_LEVEL, CALENDAR_LOG_FILE, CALENDAR_LOG_ROTATE

define("port", default=CALENDAR_PORT, help="server listen port. "
                                           "default 8080")
define("workers", default=0, help="the count of workers. "
                                  "default the same as cpu cores")
define("logfile", default=None, help="the path for log")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def sig_handler(sig, _):
    """
    signal handler
    """
    print("sig %s received" % str(sig))
    try:
        parent = psutil.Process(os.getpid())
        children = parent.children()
        for process in children:
            process.send_signal(sig)
    except (psutil.NoSuchProcess, psutil.ZombieProcess,
            psutil.AccessDenied) as ex:
        print(str(ex))
    tornado.ioloop.IOLoop.instance().add_callback(kill_server)


def kill_server():
    """
    stop the ioloop
    """
    asyncio.get_event_loop().stop()


def init_logger():
    """
    Initializes the logger settings.
    """
    formatter = logging.Formatter(CALENDAR_LOG_FMT)
    calendar_log = logging.getLogger("attendance_management_bot")
    file_handler = StreamHandler()
    file_handler.setFormatter(formatter)

    calendar_log.setLevel(CALENDAR_LOG_LEVEL)
    file_handler.addFilter(attendance_management_bot.contextlog.RequestContextFilter())
    calendar_log.addHandler(file_handler)

    logging.getLogger("tornado.application").addHandler(file_handler)
    logging.getLogger("tornado.general").addHandler(file_handler)


def check_init_bot():
    """
    Initialize bot no, check if the bot is initialized.
    If this function gets an exception, it is probably like script/registerBot.py.
    This is not executed or the execution failed.

        reference
        - https://developers.worksmobile.com/jp/document/3005001?lang=en
    """
    extra = get_init_status("bot_no")
    if extra is None:
        raise Exception("bot no init failed.")
    global_data.set_value("bot_no", extra)


def init_rich_menu_first():
    """
    Initialize rich menu API. Check also: attendance_management_bot/externals/richmenu.py

        reference
        - https://developers.worksmobile.com/jp/document/1005040?lang=en
    """
    extra = get_init_status("rich_menu")

    if extra is None:
        rich_menus = init_rich_menu(DEFAULT_LANG)
        insert_init_status("rich_menu", json.dumps(rich_menus))
    else:
        rich_menus = json.loads(extra)

    if rich_menus is None:
        raise Exception("init rich menu failed. rich_menus is None")

    rich_menu_id =rich_menus.get(RICH_MENUS[DEFAULT_LANG]["name"], None)
    if rich_menu_id is None:
        raise Exception("init rich menu failed. rich_menu_id is None")

    global_data.set_value(DEFAULT_LANG, rich_menu_id)


def init_calendar_first():
    """
    Initialize calendar API.
    """
    calendar_id = get_init_status("calendar")
    if calendar_id is None:
        calendar_id = init_calendar()
        insert_init_status("calendar", calendar_id)

    global_data.set_value(API_BO["calendar"]["name"], calendar_id)


def start_attendance_management_bot():
    """
    the attendance_management_bot launch code

    tornado.httpserver a non-blocking, single-threaded HTTP server.

        reference
        - https://www.tornadoweb.org/en/stable/httpserver.html

    tornado.routing flexible routing implementation.

        reference
        - https://www.tornadoweb.org/en/stable/routing.html

    If you use the event loop that comes with tornado, many third-party
    packages based on asyncio may not be used, such as aioredis.

    Message bot API overview.

        reference
        - https://developers.worksmobile.com/jp/document/3005001?lang=en
    """

    server = tornado.httpserver.HTTPServer(attendance_management_bot.router.getRouter())

    server.bind(options.port)
    server.start(1)

    init_logger()
    check_init_bot()
    init_rich_menu_first()
    init_calendar_first()

    asyncio.get_event_loop().run_forever()
    server.stop()
    asyncio.get_event_loop().close()

    print("exit...")
