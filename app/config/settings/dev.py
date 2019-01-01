from .local import *

import_secrets()

DEBUG = True

# Static
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# LOGGING = {
#     'disable_existing_loggers': False,
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG',
#         },
#     },
#     'loggers': {
#         'django.db': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }
