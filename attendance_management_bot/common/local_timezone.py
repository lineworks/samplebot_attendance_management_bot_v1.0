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
deal time zone
"""

__all__ = ['local_date_time']

from datetime import datetime, timedelta, timezone
from conf.config import TZone
import pytz

def local_date_time(time=None):
    """
    Time to switch UTC time to a specific time zone.

        reference
        - https://docs.python.org/3/library/datetime.html

    :param time: Time to switch time zones
    :return: local time.
    """

    if time is not None:
        date_time = datetime.utcfromtimestamp(time)
        utc_dt = date_time.replace(tzinfo=timezone.utc)
        return utc_dt.astimezone(pytz.timezone(TZone))

    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(pytz.timezone(TZone))

