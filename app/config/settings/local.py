from .base import *

import_secrets()

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '192.168.1.179',
    'amazonaws.com',
    'elasticbeanstalk.com',
]

# django-debug-toolbar
INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
