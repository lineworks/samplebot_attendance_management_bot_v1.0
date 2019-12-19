********
Source Code Description
********


Heroku automatically runs jobs defined in Procfile after deployment. The attendance management bot's Procfile initializes the environment and runs main.py to run daemons.

In this section, we'll describe functions using APIs in the attendance management bot.

Example) The source code of attendance_management_bot.externals.calendar_req.create_calendar is in the create_calendar function in attendance_management_bot/externals/calendar_req.py.

Development Language and Environment
=================

The following shows the required development environment and language:

- Python3
- Tornado framework
- Postgres

Procfile
========

https://devcenter.heroku.com/articles/procfile:

    Heroku apps include a Procfile that specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including:
    - Your app’s web server
    - Multiple types of worker processes
    - A singleton process, such as a clock
    - Tasks to run before a new release is deployed

This bot's Procfile:

.. literalinclude:: ../Procfile
    :caption: Procfile



Initialize environment
======================

.. literalinclude:: ../scripts/initialize.py
    :caption: scripts/initialize.py

Initialize database
-------------------

.. autofunction:: attendance_management_bot.initDB.init_db
    :noindex:

.. autofunction:: attendance_management_bot.initDB.create_calendar_table
    :noindex:

.. autofunction:: attendance_management_bot.initDB.create_init_status_table
    :noindex:

.. autofunction:: attendance_management_bot.initDB.create_process_status_table
    :noindex:

Register bot
------------

.. autofunction:: attendance_management_bot.registerBot.init_bot
    :noindex:

.. autofunction:: attendance_management_bot.registerBot.register_bot
    :noindex:

.. autofunction:: attendance_management_bot.registerBot.register_bot_domain
    :noindex:

Run bot
=======

.. literalinclude:: ../main.py
    :caption: main.py

.. autofunction:: attendance_management_bot.attendance_management_bot.start_attendance_management_bot
    :noindex:

.. autofunction:: attendance_management_bot.router.getRouter
    :noindex:

.. autoclass:: attendance_management_bot.callbackHandler.CallbackHandler
    :members:
    :noindex:

.. autoclass:: attendance_management_bot.check_and_handle_actions.CheckAndHandleActions
    :members:
    :noindex:

Bot API functions
=================

.. autofunction:: attendance_management_bot.model.data.make_text
    :noindex:

.. autofunction:: attendance_management_bot.model.data.make_quick_reply
    :noindex:

.. autofunction:: attendance_management_bot.model.data.make_image_carousel
    :noindex:

.. autofunction:: attendance_management_bot.externals.send_message.push_message
    :noindex:

Calender API functions
======================

.. autofunction:: attendance_management_bot.externals.calendar_req.create_calendar
    :noindex:

.. autofunction:: attendance_management_bot.externals.calendar_req.create_schedule
    :noindex:

.. autofunction:: attendance_management_bot.externals.calendar_req.modify_schedule
    :noindex:

Bot rich menu functions
=======================

.. autofunction:: attendance_management_bot.externals.richmenu.upload_content
    :noindex:

.. autofunction:: attendance_management_bot.externals.richmenu.make_add_rich_menu_body
    :noindex:

.. autofunction:: attendance_management_bot.externals.richmenu.set_rich_menu_image
    :noindex:

.. autofunction:: attendance_management_bot.externals.richmenu.set_user_specific_rich_menu
    :noindex:

.. autofunction:: attendance_management_bot.externals.richmenu.get_rich_menus
    :noindex:

.. autofunction:: attendance_management_bot.externals.richmenu.cancel_user_specific_rich_menu
    :noindex:

Bot i18n functions
===================

You can use the. /tools/gen.sh tool to generate '. Po', '. Mo' files.

    reference
    - https://docs.python.org/2/library/gettext.html
    - test/test_i18.py

execute
-------

    $ ./tools/gen.sh [filename] [po|mo] [path]

========    ===========
paramter    description
========    ===========
filename    Python source filename used to generate '.po','.mo'.
type        'po' means generate '.po' file, 'mo' means generate '.mo' file
path        Relative directory of Python source files. not ending with '/'.
========    ===========

You can find the corresponding '.po' file in 'locales/../LC_MESSAGES' according to your source file name.

step
----
1. generate '.po' file.
    ./tools/gen.sh test_i18n.py po test<br/>
    check: locales/../LC_MESSAGES/test_i18n.po
2. Multilingual string to fill in '.po' file.
3. generate '.mo' file
    ./tools/gen.sh test_i18n.py mo test<br/>
    check: locales/../LC_MESSAGES/test_i18n.mo

.. autofunction:: attendance_management_bot.model.i18n_data.get_i18n_content_by_lang
    :noindex:

.. autofunction:: attendance_management_bot.model.i18n_data.get_i18n_content
    :noindex:

.. autofunction:: attendance_management_bot.model.i18n_data.make_i18n_button
    :noindex:

.. autofunction:: attendance_management_bot.model.i18n_data.make_i18n_text
    :noindex:

.. autofunction:: attendance_management_bot.model.i18n_data.make_i18n_message_action
    :noindex:

.. autofunction:: attendance_management_bot.model.i18n_data.make_il8n_image_carousel_column
    :noindex:

Set Timezone
============

The default timezone for the attendance management bot is Asia/Tokyo, which you can change if necessary.

To change the timezone, edit #Timezone in config.py under the conf folder.

Set TZone =”{Country/City}”.

    Note
    - For TZ database names you can add as Country/City, refer to: https://developers.worksmobile.com/kr/document/1009006/v2?lang=ko

Set Language Code for Event Subject
===================================

The attendance management bot basically creates a clock-in/clock-out event subject in Japanese. If necessary, you can change the language code for event subjects to Korean or English.

To do so, edit # default language in config.py under the conf folder as shown below.

DEFAULT_LANG =”{Language code}”

    Note
    - You can choose among kr (Korean), ja (Japanese), and en (English).

Indices and tables
==================

.. toctree::
    :maxdepth: 4

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
