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
Initialize bot no.
"""

__all__ = ['create_bot', 'add_domain', 'init_bot']

import sys
import json
import psycopg2
import requests
import datetime
sys.path.append('./')
from attendance_management_bot.model.i18n_data import get_i18n_content
from attendance_management_bot.constant import PRIVATE_KEY_PATH, \
    DEVELOP_API_DOMAIN, API_BO
from attendance_management_bot.model.initStatusDBHandle \
    import insert_init_status, get_init_status
from conf.config import API_ID, DOMAIN_ID, ADMIN_ACCOUNT, LOCAL_ADDRESS, \
    SERVER_CONSUMER_KEY
from attendance_management_bot.common.token import generate_token
import gettext
_ = gettext.gettext

CALLBACK_ADDRESS = LOCAL_ADDRESS + "callback"
PHOTO_URL = LOCAL_ADDRESS + "static/icon.png"

"""
def make_i18n_name(language, name):
    return {"language": language, "name": name}

def make_i18n_description(language, description):
    return {"language": language, "description": description}
"""

def headers():
    token = generate_token()
    my_headers = {
        "consumerKey": SERVER_CONSUMER_KEY,
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    return my_headers


def register_bot(photo_address):
    """
    Register a message bot.

        reference
        - https://developers.worksmobile.com/jp/document/1005002?lang=en

    :param photo_address: Access address of user's Avatar,
        If you need to change the user image,
        please replace the corresponding file in the image/, Only PNG file.
    :return: bot no
    """

    url = "https://" + DEVELOP_API_DOMAIN + "/r/" + API_ID + "/message/v1/bot"
    fmt = _("Attendance management bot")
    a = lambda x, y: {"language": x, "name": y}
    b = lambda x, y: {"language": x, "description": y}
    data = {
        "name": "Attendance management bot",
        "i18nNames": get_i18n_content(fmt, "registerBot", function=a),
        "photoUrl": photo_address,
        "description": "Attendance management bot",
        "i18nDescriptions": get_i18n_content(fmt, "registerBot", function=b),
        "managers": [ADMIN_ACCOUNT],
        "submanagers": [],
        "useGroupJoin": False,
        "useDomainScope": False,
        "useCallback": True,
        "callbackUrl": CALLBACK_ADDRESS,
        "callbackEvents": ["text", "location", "sticker", "image"]
    }

    r = requests.post(url, data=json.dumps(data), headers=headers())
    if r.status_code != 200:
        print(r.text)
        print(r.content)
        return None
    tmp = r.json()
    print(tmp)
    return tmp["botNo"]


def register_bot_domain(bot_no):
    """
    Register a message bot domain.

        reference
        - https://developers.worksmobile.com/jp/document/1005004?lang=en

    :param bot_no: bot no
    """
    url = "https://" + DEVELOP_API_DOMAIN + "/r/" + API_ID + "/message/v1/bot/" \
          + str(bot_no) + "/domain/" + str(DOMAIN_ID)
    data = {"usePublic": True, "usePermission": False}
    r = requests.post(url, data=json.dumps(data), headers=headers())
    print(r.json())


def init_bot():
    """
    Initialize bot info. If the BOT is not registered, the system will fail to start.

    Before BOT registration,
    the system_init_status table will be queried.
    If BOT has been registered, it does not need to be re registered.
    Otherwise, the bot will be saved in the system init status table after success,
    indicating that the registration of BOT has been completed during initialization.
    """

    bot_no = get_init_status("bot_no")
    if bot_no is not None:
        print("bot no has created. bot_no:%s" % (bot_no,))
        return

    bot_no = register_bot(PHOTO_URL)
    register_bot_domain(bot_no)
    print("photo:%s" % (PHOTO_URL,))
    print("callback:%s" % (CALLBACK_ADDRESS,))
    if bot_no is not None:
        insert_init_status("bot_no", bot_no)
