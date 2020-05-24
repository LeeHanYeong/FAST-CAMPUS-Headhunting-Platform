from .base import *

AWS_SECRETS_MANAGER_SECRET_SECTION = 'fc-headhunting:local'

DEBUG = True

WSGI_APPLICATION = 'config.wsgi.local.application'
ALLOWED_HOSTS += [
    'localhost',
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
