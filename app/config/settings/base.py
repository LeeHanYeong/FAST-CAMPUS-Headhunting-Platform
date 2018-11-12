"""
Django settings for FastCampus project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from djs import import_secrets

from ..jinja2 import environment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

import_secrets()

# Static
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    STATIC_DIR,
]
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Auth
AUTH_USER_MODEL = 'members.User'

# django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = 'KO'
# PHONENUMBER_DB_FORMAT = 'NATIONAL'

# Date/Time Format
DATE_FORMAT = 'Y-m-d'

# django-modeladmin-reorder
ADMIN_REORDER = (
    {'app': 'members', 'label': '사용자 관리', 'models': (
        'members.ApplicantUser',
        'members.CompanyUser')},
    {'app': 'members', 'label': '이력서 항목 관리', 'models': (
        'members.Link',
        'members.Skill',
    )},
    {'app': 'courses', 'label': '과정 관리', 'models': (
        'courses.Course',
        'courses.CoursePeriod',
    )},
)

# compressor
COMPRESS_JINJA2_GET_ENVIRONMENT = environment

INSTALLED_APPS = [
    'courses.apps.CoursesConfig',
    'members.apps.MembersConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'admin_reorder',
    'django_extensions',
    'phonenumber_field',
    'rest_framework',
    'sass_processor',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            TEMPLATES_DIR,
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [],
            'environment': 'config.jinja2.environment',
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True
