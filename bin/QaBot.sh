#!/usr/bin/env bash

echo 'This script has been deprecated, try run componets manually please...:('

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
        sleep 1
        screen -list
        ;;
    stop)
        screen -S Django-Qabot -X kill
        sleep 1
        screen -list
        ;;
    status)
        screen -list
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    debug)
        screen -r Django-Qabot
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|debug}"
        ;;
esac
