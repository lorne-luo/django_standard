"""
Django settings project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

import os
import time

import environ

root = environ.Path(__file__) - 3  # (/config/settings/base.py - 3 = /)

BASE_DIR = root()

STARTUP_TIMESTAMP = int(time.time())

# Load operating system environment variables and then prepare to use them
env = environ.Env()
env_file = root('.env')
if os.path.exists(env_file):
    env.read_env(env_file)

# AUTH & USER
BASE_URL = env('BASE_URL')
AUTH_USER_MODEL = 'auth_user.User'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/dashboard/'
BASE_CMS_URL=env('BASE_CMS_URL')
SITE_ID = 1

# APP CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps

INSTALLED_APPS = [
    # DJANGO_APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # THIRD_PARTY_APPS
    'django_nose',
    'pinax.stripe',
    'django_ses',
    'captcha',
    'rest_framework',

    # LOCAL_APPS
    'apps.auth_user',
]

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    # IP restriction
    'allow_cidr.middleware.AllowCIDRMiddleware',

    # django
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.django.context_processors.global_settings',
            ],
        },
    },
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types

DATABASES = {
    'default': env.db('DATABASE_URL', default='mysql://developer:butterfly@db.butterfly.com.au:3306/db_name_example')
}

DATABASES['default']['OPTIONS'] = {
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug

DEBUG = env.bool('DEBUG', False)

# URL Configuration
# ------------------------------------------------------------------------------

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------

EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='dev+stylelab-qa@butterfly.com.au')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins

ADMINS = env.list('ADMINS', default=['butterflynet@butterfly.com.au'])

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Melbourne'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# AUSTRALIA DATE FORMAT
DATE_FORMAT = "d M Y"

SHORT_DATE_FORMAT = "d M Y"

DATETIME_FORMAT = "h:i A, d M Y"

SHORT_DATETIME_FORMAT = "h:i A"

# STATIC FILES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    root('static'),
]

STATIC_ROOT = root('staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = root('media')
MEDIA_URL = '/media/'

# TEST
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# AWS
# ------------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
# S3
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default="ap-southeast-2")
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# SES
AWS_SES_REGION_NAME = env('AWS_SES_REGION_NAME', default='us-east-1')
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'

# STRIPE INTEGRATION VIA PINAX_STRIPE
# ------------------------------------------------------------------------------
PINAX_STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
PINAX_STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
PINAX_STRIPE_API_VERSION = "2015-10-16"
PINAX_STRIPE_SUBSCRIPTION_TAX_PERCENT = 10

# reCAPTCHA
# ------------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True  # enable no captcha

# Google Analytic
GOOGLE_TAG_MANAGER = env('GOOGLE_TAG_MANAGER', default='')

# Terms of use and privacy policy
TERMS_OF_USE_URL = env('TERMS_OF_USE_URL')
PRIVACY_POLICY_URL = env('PRIVACY_POLICY_URL')
CONTACT_URL = env('CONTACT_URL')

# PROJECT SETTINGS
# ------------------------------------------------------------------------------

# All your project settings go here
