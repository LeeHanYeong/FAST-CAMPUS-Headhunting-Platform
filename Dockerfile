FROM        azelf/fc-headhunting:base
MAINTAINER  dev@lhy.kr

ENV         DJANGO_SETTINGS_MODULE  config.settings.production

COPY        ./  /srv/project
WORKDIR     /srv/project

# Nginx
RUN         rm -rf  /etc/nginx/sites-available/* && \
            rm -rf  /etc/nginx/sites-enabled/* && \
            cp -f   /srv/project/.config/app.nginx \
                    /etc/nginx/sites-available/ && \
            ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

# supervisor설정파일 복사
RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

WORKDIR     /srv/project/app
EXPOSE      80
CMD         supervisord -n