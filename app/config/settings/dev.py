from .local import *

AWS_SECRETS_MANAGER_SECRET_SECTION = 'fc-headhunting:dev'

ALLOWED_HOSTS += [
    'amazonaws.com',
    'elasticbeanstalk.com',

]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
