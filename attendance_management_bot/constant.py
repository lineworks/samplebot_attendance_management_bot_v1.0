#!/bin/bash python3
# -*- coding: UTF-8 -*-
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
constants.py Defining the constant used for a project.

"""
import os
from conf.config import *
# ---------------------------------------------------------------------
# Constants and global variables
# ---------------------------------------------------------------------

# ROOT PATH
ABSDIR_OF_SELF = os.path.dirname(os.path.abspath(__file__))
ABSDIR_OF_PARENT = os.path.dirname(ABSDIR_OF_SELF)

HEROKU_SERVER_ID = SERVER_ID
PRIVATE_KEY_PATH = ABSDIR_OF_PARENT + "/key/" + SECRET_KEY_NAME

# DOMAIN
STORAGE_DOMAIN = "storage.worksmobile.com"
AUTH_DOMAIN = "auth.worksmobile.com"
DEVELOP_API_DOMAIN = "apis.worksmobile.com"

# RICH_MENUS
RICH_MENUS = {
                'en':
                    {
                        "name": "attendance_management_bot_rich_menu_en",
                        "path": ABSDIR_OF_PARENT + "/image/en/Rich_Menu.png"
                    },
                'ko':
                    {
                        "name": "attendance_management_bot_rich_menu_kr",
                        "path": ABSDIR_OF_PARENT + "/image/kr/Rich_Menu.png"
                    },
                'ja':
                    {
                        "name": "attendance_management_bot_rich_menu_jp",
                        "path": ABSDIR_OF_PARENT + "/image/jp/Rich_Menu.png"
                    }

             }

# IMAGE CAROUSEL
IMAGE_CAROUSEL = {
                    "en":
                    [
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_01.png",
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_02.png",
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_03.png"
                    ],
                    "ko":
                    [
                        LOCAL_ADDRESS + "static/kr/IMG_Carousel_01.png",
                        LOCAL_ADDRESS + "static/kr/IMG_Carousel_02.png",
                        LOCAL_ADDRESS + "static/kr/IMG_Carousel_03.png"
                    ],
                    "ja":
                    [
                        LOCAL_ADDRESS + "static/jp/IMG_Carousel_01.png",
                        LOCAL_ADDRESS + "static/jp/IMG_Carousel_02.png",
                        LOCAL_ADDRESS + "static/jp/IMG_Carousel_03.png"
                    ]
                }

# API ADDRESS
API_BO = {
            "headers": {
                "content-type": "application/json",
                "charset": "UTF-8"
            },
            "upload_url": "http://" + STORAGE_DOMAIN
                          + "/openapi/message/upload.api",
            "push_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                        + API_ID + "/message/v1/bot/_BOT_NO_/message/push",
            "rich_menu_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                             + API_ID + "/message/v1/bot/_BOT_NO_/richmenu",

            "calendar":
            {
                "name": "calendar bot",
                "create_calendar_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_ACCOUNT_ID_/"
                                       "calendarList",
                "create_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_ACCOUNT_ID_/calendars/"
                                       "_CALENDAR_ID_/events",
                "modify_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_ACCOUNT_ID_/calendars/"
                                       "_CALENDAR_ID_/events/_CALENDAR_UUID_",
            },

            "TZone":
            {
                "contacts_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                    + API_ID
                                    + "/contact/v2/accounts/_USER_ACCOUNT_ID_"
            },
            "auth_url": "https://" + AUTH_DOMAIN + "/b/" + API_ID
                        + "/server/token?grant_type=urn%3Aietf%3Aparams%3Aoauth"
                          "%3Agrant-type%3Ajwt-bearer&assertion="
        }

# OPEN API
OPEN_API = {
        "_info": "nwetest.com",
        "apiId": API_ID,
        "consumerKey": SERVER_CONSUMER_KEY
    }

# DB CONFIG
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "sslmode": "prefer"
}

# FILE SYSTEM
FILE_SYSTEM = {
    "image_dir": ABSDIR_OF_PARENT+"/image",
}
