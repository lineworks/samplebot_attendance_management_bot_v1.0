#!/bin/env bash

# supervisord and attendance_management_bot logs are auto cleaned.
# see the configure files for them.

# remove out of date attendance_management_bot logs and compress log
clover_log_path=/home1/irteam/logs/attendance_management_bot/
find $attendance_management_bot_log_path -mtime +50 -name 'attendance_management_bot.log.*.xz' -delete
find $attendance_management_bot_log_path -name 'attendance_management_bot.log.*-*' -not -name 'attendance_management_bot.log.*.xz' -execdir xz -z -T4 {} \;
