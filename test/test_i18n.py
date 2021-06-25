# -*- coding: utf-8 -*-
"""
test i18n content
"""

__all__ = ['get_data', 'test_ko']

import gettext
_ = gettext.gettext


def get_data():
    """
    Generate multilingual key string.

        reference
        - https://docs.python.org/2/library/gettext.html

    :return: Multilingual key string.
    """
    return _("Hello, I'm an attendance management "
             "bot of WORKS that helps your "
             "timeclock management and entry.")


def test_ko():
    """
    Load multilingual strings.

        reference
        - https://docs.python.org/2/library/gettext.html

    """
    original = get_data()
    ko = gettext.translation('base', 'locales', ['ko'])
    en = gettext.translation('base', 'locales', ['en'])
    ja = gettext.translation('base', 'locales', ['ja'])
    assert ko.gettext(original).startswith(u'안녕하세요')
    assert ja.gettext(original).startswith(u'こんにちは。')
    assert en.gettext(original).startswith('Hello, ')
