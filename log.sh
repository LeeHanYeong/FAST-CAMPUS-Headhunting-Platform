#!/usr/bin/env bash
CMD='sudo docker exec $(sudo docker ps -q) tail -f'
LOG_ERROR='/srv/project/.log/error.log'
LOG_INFO='/srv/project/.log/info.log'
LOG_NGINX_ERROR='/var/log/nginx/error.log'
LOG_NGINX_ACCESS='/var/log/nginx/access.log'
LOG_UWSGI='/var/log/uwsgi.log'

eb ssh --command "$CMD $LOG_ERROR $LOG_NGINX_ERROR $LOG_UWSGI"
