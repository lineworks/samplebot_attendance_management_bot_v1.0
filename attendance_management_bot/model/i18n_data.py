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
create i18n message content
"""

__all__ = ['get_i18n_content', 'get_i18n_content_by_lang', 'make_i18n_button',
           'make_i18n_text', 'make_i18n_message_action',
           'make_i18n_postback_action', 'make_il8n_image_carousel_column']

import json
from attendance_management_bot.constant import IMAGE_CAROUSEL
from attendance_management_bot.model.data import *
import gettext
import locale
_ = gettext.gettext


def get_i18n_content(fmt, local, **kw):
    """
    Get multilingual data structure according to format parameter id.

        reference
        - https://docs.python.org/2/library/gettext.html

    :param fmt: Multilingual key string. like _('This is a translatable string.')
    :param local: Domain corresponding to "fmt".
    :param kw: Named variable parameter list.
        Common parameters:
            function: A callback function used to encapsulate multiple languages.
            fmt1: The key string is the multilingual parameter of the substring in the format string. Used to format dates.
            date: Local time of datetime object.
    :return:
        If the parameter contains the package function of the package, An encapsulated multilingual dictionary object will be returned.
        If the parameter does not contain a package function, this returns a Multilingual list object.
    """
    ko = gettext.translation(local, 'locales', ['ko'])
    en = gettext.translation(local, 'locales', ['en'])
    ja = gettext.translation(local, 'locales', ['ja'])

    i18n_content = {}
    function = None
    if 'function' in kw:
        function = kw['function']
        if function is not None:
            i18n_content = []

    fmt1 = None
    if 'fmt1' in kw:
        fmt1 = kw['fmt1']

    date = None
    if 'date' in kw:
        date = kw['date']

    for lang in [('en_US', en), ('ja_JP', ja), ('ko_KR', ko)]:
        if fmt1 is not None and date is not None:
            locale.setlocale(locale.LC_TIME,
                             "{lang}{code}".format(lang=lang[0], code=".utf8"))
            kw['date'] = date.strftime(lang[1].gettext(fmt1))

        if function is not None:
            if len(kw) > 0:
                i18n_content_item = function(lang[0],
                                             lang[1].gettext(fmt).format(**kw))
            else:
                i18n_content_item = function(lang[0],
                                             lang[1].gettext(fmt))

            i18n_content.append(i18n_content_item)
        elif len(kw) > 0:
            i18n_content[lang[0]] = lang[1].gettext(fmt).format(**kw)
        else:
            i18n_content[lang[0]] = lang[1].gettext(fmt)
    locale.setlocale(locale.LC_TIME,
                     "{lang}{code}".format(lang='en_US', code=".utf8"))
    return i18n_content


def get_i18n_content_by_lang(fmt, local, lang, **kw):
    """
    Get another language string according to key string.

        reference
        - https://docs.python.org/2/library/gettext.html

    :param fmt: Multilingual key string. like _('This is a translatable string.')
    :param local: Domain corresponding to "fmt".
    :param lang: Language. ['en', 'ko', 'ja']
    :param kw: Named variable parameter list.
        fmt1: The key string is the multilingual parameter of the substring in the format string. Used to format dates.
        date: Local time of datetime object.
    :return: a string.
    """
    local_map = {'en': 'en_US', 'ja': 'ja_JP', 'ko': 'ko_KR'}
    local_text = gettext.translation(local, 'locales', [lang])

    date = None
    if 'date' in kw:
        date = kw['date']

    fmt1 = None
    if 'fmt1' in kw:
        fmt1 = kw['fmt1']

    if date is not None and fmt1 is not None:
        locale.setlocale(locale.LC_TIME,
                         "{lang}{code}".format(lang=local_map[lang],
                                               code=".utf8"))
        kw['date'] = date.strftime(local_text.gettext(fmt1))

    del kw['fmt1']
    if len(kw) > 0:
        content = local_text.gettext(fmt).format(**kw)
    else:
        content = local_text.gettext(fmt)
    locale.setlocale(locale.LC_TIME,
                     "{lang}{code}".format(lang='en_US', code=".utf8"))
    return content


def make_i18n_button(text, actions, local, fmt):
    """
    Create a multilingual button object.

        reference
        - https://developers.worksmobile.com/jp/document/100500804?lang=en
        - Check also: attendance_management_bot/model/data.py::make_button
    """
    i18n_texts = get_i18n_content(fmt, local, function=make_i18n_content_texts)
    return make_button(text, actions, content_texts=i18n_texts)


def make_i18n_text(text, local, fmt, **kw):
    """
    Create a multilingual text object.

        reference
        - https://developers.worksmobile.com/jp/document/100500801?lang=en
        - Check also: attendance_management_bot/model/data.py::make_text
    """
    i18n_texts = get_i18n_content(fmt, local, function=i18n_text, **kw)
    return make_text(text, i18n_texts=i18n_texts)


def make_i18n_message_action(post_back, local, label, fmt_label=None,
                             text=None, fmt_text=None):
    """
    Create a multilingual message action object.

        reference
        - https://developers.worksmobile.com/jp/document/1005050?lang=en
        - Check also: attendance_management_bot/model/data.py::make_message_action
    """
    i18n_labels = None
    if fmt_label is not None:
        i18n_labels = get_i18n_content(fmt_label, local,
                                       function=make_i18n_label)

    i18n_texts = None
    if fmt_text is not None:
        i18n_texts = get_i18n_content(fmt_text, local, function=i18n_text)
    return make_message_action(post_back, label, i18n_labels=i18n_labels,
                               text=text, i18n_texts=i18n_texts)


def make_i18n_postback_action(post_back, local, label, fmt_label=None,
                              text=None, fmt_text=None):
    """
    Create a multilingual postback action object.

        reference
        - https://developers.worksmobile.com/jp/document/1005050?lang=en
        - Check also: attendance_management_bot/model/data.py::make_postback_action
    """
    i18n_labels = None
    if fmt_label is not None:
        i18n_labels = get_i18n_content(fmt_label, local,
                                       function=make_i18n_label)

    i18n_texts = None
    if fmt_text is not None:
        i18n_texts = get_i18n_content(fmt_text, local,
                                      function=i18n_display_text)

    return  make_postback_action(post_back, label, i18n_labels,
                                 text, i18n_texts)


def make_il8n_image_carousel_column(number, action):
    """
    Create a multilingual image carousel column object.

        reference
        - https://developers.worksmobile.com/jp/document/100500809?lang=en
        - Check also: attendance_management_bot/model/data.py::make_image_carousel_column
    """
    i18n_images = []
    for lang in [('en_US', 'en'), ('ja_JP', 'ja'), ('ko_KR', 'ko')]:
        i18n_image_item = make_i18n_image_url(lang[0],
                                              IMAGE_CAROUSEL[lang[1]][number])
        i18n_images.append(i18n_image_item)

    return make_image_carousel_column(image_url=IMAGE_CAROUSEL['en'][number],
                                      action=action,
                                      i18n_image_urls=i18n_images)

