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
Provides calendar API related functions
"""

__all__ = ['make_icalendar_data', 'create_calendar', 'create_schedule',
           'modify_schedule', 'init_calendar']

import io
import logging
import json
import pytz
import uuid
import tornado.gen
from tornado.web import HTTPError
from datetime import datetime, timezone
from icalendar import Calendar, Event, Timezone, TimezoneStandard
from attendance_management_bot.common.utils \
    import auth_get, auth_post, auth_put
from conf.config import TZone
from attendance_management_bot.constant import API_BO, \
    OPEN_API, ADMIN_ACCOUNT, DOMAIN_ID
from attendance_management_bot.common.global_data import get_value

LOGGER = logging.getLogger("attendance_management_bot")


def create_headers():
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    return headers


def make_icalendar_data(uid, summary, current, end, begin,
                        account_id, create_flag=False):
    """
    Generate iCalendar data format message body.

        reference
        - https://developers.worksmobile.com/jp/document/1007011?lang=en
    """

    cal = Calendar()
    cal.add('PRODID', 'Works sample bot Calendar')
    cal.add('VERSION', '2.0')

    standard = TimezoneStandard()
    standard.add('DTSTART', datetime(1970, 1, 1, 0, 0, 0,
                                     tzinfo=pytz.timezone(TZone)))
    standard.add('TZOFFSETFROM', current.utcoffset())
    standard.add('TZOFFSETTO', current.utcoffset())
    standard.add('TZNAME', current.tzname())

    tz = Timezone()
    tz.add_component(standard)
    tz.add('TZID', tz)

    event = Event()
    event.add('UID', uid)

    if create_flag:
        event.add('CREATED', current)

    event.add('DESCRIPTION', account_id)
    event.add('SUMMARY', summary)
    event.add('DTSTART', begin)
    event.add('DTEND', end)
    event.add('LAST-MODIFIED', current)
    event.add('DTSTAMP', current)

    cal.add_component(event)
    cal.add_component(tz)
    schedule_local_string = bytes.decode(cal.to_ical())
    LOGGER.info("schedule:%s", schedule_local_string)
    return schedule_local_string


def create_calendar():
    """
    create calender.

        reference
        - https://developers.worksmobile.com/jp/document/100702701?lang=en

    :return: calendar id.
    """
    body = {
        "name": "Attendance management bot",
        "description": "Attendance management bot",
        "invitationUserList": [{
            "email": ADMIN_ACCOUNT,
            "actionType": "insert",
            "roleId": 2
        }]
    }

    headers = create_headers()
    url = API_BO["calendar"]["create_calendar_url"]
    url = url.replace("_ACCOUNT_ID_", ADMIN_ACCOUNT)
    LOGGER.info("create calendar. url:%s body:%s", url, str(body))

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("create calendar failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("create calendar id. http response code error.")

    LOGGER.info("create calendar id. url:%s txt:%s body:%s",
                url, response.text, response.content)
    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("create calendar failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise Exception("create calendar id. response no success.")
    return tmp_req["returnValue"]


def create_schedule(current, end, begin, account_id, title):
    """
    create schedule.

        reference
        - https://developers.worksmobile.com/jp/document/100702703?lang=en

    :return: schedule id.
    """

    uid = str(uuid.uuid4()) + account_id
    schedule_data = make_icalendar_data(uid, title, current,
                                        end, begin, account_id, True)
    body = {
        "ical": schedule_data
    }

    calendar_id = get_value(API_BO["calendar"]["name"], None)
    if calendar_id is None:
        LOGGER.error("get calendar from cached failed.")
        raise HTTPError(500, "internal error. get calendar is failed.")

    headers = create_headers()
    url = API_BO["calendar"]["create_schedule_url"]
    url = url.replace("_ACCOUNT_ID_", ADMIN_ACCOUNT)
    url = url.replace("_CALENDAR_ID_", calendar_id)

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("create schedules failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule http code error.")

    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. http response error.")

    LOGGER.info("create schedule. url:%s text:%s body:%s",
                 url, response.text, response.content)

    return_value = tmp_req.get("returnValue", None)
    if return_value is None:
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule content error.")

    schedule_uid = return_value.get("icalUid", None)
    if schedule_uid is None:
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule content error.")
    return schedule_uid


def modify_schedule(calendar_uid, current, end, begin, account_id, title):
    """
    modify schedule.

        reference
        - https://developers.worksmobile.com/jp/document/100702704?lang=en

    :return: schedule id.
    """

    calendar_data = make_icalendar_data(calendar_uid, title,
                                        current, end, begin, account_id)
    body = {
        "ical": calendar_data
    }

    calendar_id = get_value(API_BO["calendar"]["name"], None)
    if calendar_id is None:
        LOGGER.error("get calendar from cached failed.")
        raise HTTPError(500, "internal error. get calendar is failed.")

    url = API_BO["calendar"]["modify_schedule_url"]
    url = url.replace("_ACCOUNT_ID_", ADMIN_ACCOUNT)
    url = url.replace("_CALENDAR_ID_", calendar_id)
    url = url.replace("_CALENDAR_UUID_", calendar_uid)

    headers = create_headers()
    response = auth_put(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("modify schedules failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500,
                        "internal error. create schedule http code error.")

    LOGGER.info("modify schedules. url:%s text:%s body:%s",
                 url, response.text, response.content)

    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("modify schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. http response error.")


def init_calendar():
    """
    init calendar.
    The calendar initialization function is called to generate
    the calendar id when the system starts.

    :return: calendar id
    """
    calendar_id = create_calendar()
    if calendar_id is None:
        raise Exception("init calendar failed.")
    return calendar_id
