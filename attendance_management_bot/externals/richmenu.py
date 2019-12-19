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
rich menu's api
"""

__all__ = ['upload_content', 'make_add_rich_menu_body', 'set_rich_menu_image',
           'set_user_specific_rich_menu', 'get_rich_menus',
           'cancel_user_specific_rich_menu', 'init_rich_menu']

import io
import logging
import json
from attendance_management_bot.model.data import make_size, make_bound, \
    make_add_rich_menu, make_area
from attendance_management_bot.model.i18n_data import make_i18n_postback_action
from attendance_management_bot.common import utils
from attendance_management_bot.constant import API_BO, OPEN_API, RICH_MENUS
import tornado.gen
from attendance_management_bot.common.utils import auth_get, auth_post, auth_del
import gettext
_ = gettext.gettext

LOGGER = logging.getLogger("attendance_management_bot")


def upload_content(file_path):
    """
    Upload rich menu background picture.

        reference
        - https://developers.worksmobile.com/jp/document/1005025?lang=en

    :param file_path: resource local path
    :return: resource id
    """
    headers = {
        "consumerKey": OPEN_API["consumerKey"],
        "x-works-apiid": OPEN_API["apiId"]
    }

    files = {'resourceName': open(file_path, 'rb')}

    url = API_BO["upload_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("upload content . url:%s", url)

    response = auth_post(url, files=files, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("upload content. http return error.")
    if "x-works-resource-id" not in response.headers:
        LOGGER.error("invalid content. url:%s txt:%s headers:%s",
                    url, response.text, response.headers)
        raise Exception("upload content. not fond 'x-works-resource-id'.")
    return response.headers["x-works-resource-id"]


def make_add_rich_menu_body(rich_menu_name):
    """
    add rich menu body

        reference
        - https://developers.worksmobile.com/jp/document/100504001?lang=en

    :param rich_menu_name: rich menu name
    :return: rich menu id
    """
    size = make_size(2500, 1686)

    fmt0 = _("Record clock-in")
    bound0 = make_bound(0, 0, 1250, 1286)
    action0 = make_i18n_postback_action("sign_in", "richmenu", "Record clock-in",
                                   fmt0, "Record clock-in", fmt0)

    fmt1 = _("Record clock-out")
    bound1 = make_bound(1250, 0, 1250, 1286)
    action1 = make_i18n_postback_action("sign_out", "richmenu", "Record clock-out",
                                   fmt1, "Record clock-out", fmt1)

    fmt2 = _("Start over")
    bound2 = make_bound(0, 1286, 2500, 400)
    action2 = make_i18n_postback_action("to_first", "richmenu", "Start over",
                                   fmt2, "Start over", fmt2)

    rich_menu = make_add_rich_menu(
                    rich_menu_name,
                    size,
                    [
                        make_area(bound0, action0),
                        make_area(bound1, action1),
                        make_area(bound2, action2)
                    ])

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("register richmenu. url:%s", url)

    response = auth_post(url, data=json.dumps(rich_menu), headers=headers)
    if response.status_code != 200:
        LOGGER.info("register richmenu failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("register richmenu. http return error.")

    LOGGER.info("register richmenu success. url:%s txt:%s body:%s",
                url, response.text, response.content)

    tmp = json.loads(response.content)
    return tmp["richMenuId"]


def set_rich_menu_image(resource_id, rich_menu_id):
    """
    Set a rich menu image.

        reference
        - https://developers.worksmobile.com/jp/document/100504002?lang=en

    :param resource_id: resource id
    :param rich_menu_id: rich menu id
    :return:
    """
    body = {"resourceId": resource_id}

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"] + "/" + rich_menu_id + "/content"
    url = utils.replace_url_bot_no(url)
    LOGGER.info("set rich menu image . url:%s", url)

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.info("set rich menu image failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set richmenu image. http return error.")

    LOGGER.info("set rich menu image success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def set_user_specific_rich_menu(rich_menu_id, account_id):
    """
    Set a user-specific rich menu.

        reference
        - https://developers.worksmobile.com/jp/document/100504010?lang=en

    :param rich_menu_id: rich menu id
    :param account_id: user account id
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/" \
          + rich_menu_id + "/account/" + account_id

    url = utils.replace_url_bot_no(url)

    response = auth_post(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set user specific richmenu. http return error.")
    LOGGER.info("set user specific richmenu success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def get_rich_menus():
    """
    Get rich menus

        reference
        - https://developers.worksmobile.com/jp/document/100504004?lang=en

    :return: rich menu list
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("push message begin. url:%s", url)
    response = auth_get(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        return None

    LOGGER.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)

    tmp = json.loads(response.content)
    if "richmenus" in tmp:
        return tmp["richmenus"]

    return None


def cancel_user_specific_rich_menu(account_id):
    """
    Cancel a user-specific rich menu

        reference
        - https://developers.worksmobile.com/jp/document/100504012?lang=en

    :param account_id: user account id
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/account/" + account_id
    url = utils.replace_url_bot_no(url)

    response = auth_del(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("canncel user specific richmenu. http return error.")
    LOGGER.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def init_rich_menu(local):
    """
    init rich menu.

        reference
        - https://developers.worksmobile.com/jp/document/1005040?lang=en

    :return: rich menu id
    """
    if local is None or local not in RICH_MENUS:
        raise Exception("init rich menus failed. default language error.")

    il8n_rich_menu_id = {}
    rich_menus = get_rich_menus()
    if rich_menus is not None:
        for menu in rich_menus:
            if str(menu["name"]) == RICH_MENUS[local]["name"]:
                il8n_rich_menu_id[RICH_MENUS[local]["name"]] = \
                    menu["richMenuId"]
                return il8n_rich_menu_id

    rich_menu_id = make_add_rich_menu_body(RICH_MENUS[local]["name"])
    resource_id = upload_content(RICH_MENUS[local]["path"])
    set_rich_menu_image(resource_id, rich_menu_id)
    il8n_rich_menu_id[RICH_MENUS[local]["name"]] = rich_menu_id

    return il8n_rich_menu_id