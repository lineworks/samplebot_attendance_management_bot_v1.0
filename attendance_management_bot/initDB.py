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
Initialize the data structure.
"""

__all__ = ['create_calendar_table', 'create_init_status_table',
           'create_process_status_table', 'init_db']

import json
import psycopg2
import psycopg2.extras as extras
from psycopg2.errors import DuplicateTable, DuplicateObject
from attendance_management_bot.constant import DB_CONFIG


def create_calendar_table():
    """
    create calendar table.
    Save the user's check-in and check-out schedule information.

    =========== ===================================================================================
    column      description
    =========== ===================================================================================
    schedule_id schedule id, The bot will create a daily schedule for each user who sign in and out.
    account     user account id.
    cur_date    current date by local time.
    begin_time  schedule begin time.
    end_time    schedule end time.
    create_time record creation time.
    =========== ===================================================================================
    """

    create_sql = '''
                CREATE TABLE IF NOT EXISTS bot_calendar_record( 
                 schedule_id  varchar(128)      NOT NULL, 
                 account      varchar(64)       NOT NULL, 
                 cur_date     date              NOT NULL, 
                 begin_time   bigint            NOT NULL, 
                 end_time     bigint            NOT NULL, 
                 create_time  timestamp         NOT NULL 
                 default current_timestamp, 
                 update_time  timestamp         NOT NULL 
                 default current_timestamp, 
                 PRIMARY KEY (schedule_id));
                 '''

    index_sql = '''CREATE UNIQUE INDEX account_time 
                ON bot_calendar_record(account, cur_date);'''

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(create_sql)
                cur.execute(index_sql)
            except DuplicateTable:
                pass


def create_init_status_table():
    """
    create init status table, Save system initialization information(register bot,
    register rich menu, create calender).

    =========== ===========
    column      description
    =========== ===========
    action      Initialized item (bot no, rich menu, calender id, ...),
    extra       Initialized data or status,
    create_time record creation time
    =========== ===========
    """
    create_sql = ''' 
                CREATE TABLE IF NOT EXISTS system_init_status( 
                 action       varchar(64)   NOT NULL, 
                 extra      varchar(128)     DEFAULT NULL, 
                 create_time  TIMESTAMP     NOT NULL 
                 DEFAULT      CURRENT_TIMESTAMP, 
                 update_time  TIMESTAMP         NOT NULL 
                 default      CURRENT_TIMESTAMP, 
                 PRIMARY KEY (action));
                '''

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)


def create_process_status_table():
    """
    create types and status tables. Save user's status information.

    m_status: Is a enum type value，

    =========== ===========
    type        description
    =========== ===========
    wait_in     Waiting for the user to enter the check-in time status.
    in_done     User input check-in time completed.
    wait_out    Waiting for the user to enter the check-out time status.
    out_done    User input check-out time completed.
    =========== ===========

    m_process: Is a enum type value

    =============   ===========
    type            description
    =============   ===========
    sign_in_done    Check-in operation completed.
    sign_out_done   Check-out operation completed.
    =============   ===========

    If the type already exists, the duplicateobject exception will be thrown.

    bot_process_status table

    =========== ===========
    column      description
    =========== ===========
    account     user account id,
    cur_date    current date by local time,
    status      is m_status value,
    process     is m_process value,
    create_time record creation time
    =========== ===========
    """
    status_type_sql = '''
                        CREATE TYPE m_status AS  
                            ENUM('none', 'wait_in', 'in_done', 
                            'wait_out', 'out_done');
                      '''

    process_type_sql = '''
                        CREATE TYPE m_process AS 
                           ENUM('none', 'sign_in_done', 'sign_out_done');
                       '''

    create_sql = '''
                CREATE TABLE IF NOT EXISTS bot_process_status( 
                 account      varchar(64)   NOT NULL,  
                 cur_date     date          NOT NULL,  
                 status       m_status      DEFAULT NULL,  
                 process      m_process     DEFAULT NULL,  
                 create_time  timestamp     NOT NULL  
                 default current_timestamp,  
                 update_time  timestamp         NOT NULL  
                 default current_timestamp, 
                 PRIMARY KEY (account, cur_date));
                 '''

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(status_type_sql)
                cur.execute(process_type_sql)
                cur.execute(create_sql)
            except DuplicateObject:
                print("bot_process_status is DuplicateObject. please check it.")
                pass
            except DuplicateTable:
                pass

def init_db():
    """
    Initialize the data structure.

    Table list:

    - bot_calendar_record
    - system_init_status
    - bot_process_status
    """
    create_calendar_table()
    create_init_status_table()
    create_process_status_table()
