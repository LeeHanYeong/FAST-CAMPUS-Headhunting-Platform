from .local import *

AWS_SECRETS_MANAGER_SECRET_SECTION = 'fc-headhunting:dev'
ALLOWED_HOSTS += SECRETS['ALLOWED_HOSTS']

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Static
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

# DB
DATABASES = SECRETS['DATABASES']
