from __future__ import absolute_import, unicode_literals

from .base import *

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '.butterfly.com.au', ])

ALLOWED_CIDR_NETS = env.list('ALLOWED_CIDR_NETS', default=['192.168.1.0/24'])

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

EMAIL_BACKEND = 'django_ses.SESBackend'
