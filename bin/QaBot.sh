#!/usr/bin/env bash

QABOT_HOME="`pwd`/.."
WXBOT_HOME="`pwd`/../lib/wxBot"
QASNAKE_HOME="`pwd`/../lib/QA-Snake/QA"

SH='/usr/bin/env bash'
PY2='/usr/bin/env python2'
PY3='/usr/bin/env python3'

case "$1" in
start)
      cd $QABOT_HOME
      screen -dmS Django-Qabot $PY3 manage.py runserver

      $0 status
   ;;
stop)
      screen -S Django-Qabot -X kill

      $0 status
   ;;
status)
      screen -list
   ;;
restart)
      $0 stop
      $0 start
   ;;
*)
      echo "Usage: $0 {start|stop|restart|status}"
   ;;
esac



