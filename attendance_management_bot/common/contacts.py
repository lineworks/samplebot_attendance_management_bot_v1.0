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
get a user info by account id.
"""

__all__ = ['get_user_info_by_account']

from attendance_management_bot.common.utils import auth_get, auth_post
from attendance_management_bot.constant import API_BO, OPEN_API
from tornado.web import HTTPError
import logging
import pytz
import json

LOGGER = logging.getLogger("attendance_management_bot")

def get_user_info_by_account(account_id):
    """
    Get user info of account.

        reference
        - https://developers.worksmobile.com/jp/document/1006004/v1?lang=en

    If you fail to get external key,
    log in to the development console to check your configuration.

        reference
        - https://auth.worksmobile.com/login/login?

    accessUrl=https%3A%2F%2Fdevelopers.worksmobile.com
    %3A443%2Fconsole%2Fopenapi%2Fmain)

    :return: external key
    """
    contacts_url = API_BO["TZone"]["contacts_url"]
    contacts_url = contacts_url.replace("_USER_ACCOUNT_ID_", account_id)
    
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "consumerKey": OPEN_API["consumerKey"]
    }

    response = auth_get(contacts_url, headers=headers)
    if response.status_code != 200 or response.content is None:
        LOGGER.error("get user info failed. url:%s text:%s body:%s",
                    contacts_url, response.text, response.content)
        raise HTTPError(500, "get user info. http return code error.")
    tmp_req = json.loads(response.content)
    name = tmp_req.get("name", None)
    if name is None:
        raise HTTPError(500, "internal error. name filed is none")
    return name
