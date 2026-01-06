"""
Django settings for printmanager project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from datetime import timedelta
import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '10b7c805-dc11-4984-ab08-cd2884aec0dd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

 
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.43.226',
    '46.210.214.105'
]

DB_DEBUG = True


ENVIRONMENT_DEV = os.environ.get('ENV') == 'debug'

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'app',
    'jobs',
    'watcher',
    'generator',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'printmanager.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
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
]

WSGI_APPLICATION = 'printmanager.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
 

if DB_DEBUG == True :
    DATABASES = {           
             'default': {        
                'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'teudot',  # Or path to database file if using sqlite3.
                'USER': 'postgres',  
                'PASSWORD': 'Aa123456',  
                'HOST': '192.168.43.226',    #'HOST': '88.198.76.191',  
                'PORT': '5432',  
            },
    }
else :
    DATABASES = { 
            'default': {        
                'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'teudot',  # printmanager Or path to database file if using sqlite3.
                'USER': 'manaadmin',  
                'PASSWORD': '**********',  
                'HOST': '',#'91.107.209.254',#'10.11.20.51',  
                'PORT': '5432',  
            },
    }
    # 




# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))


# Celery settings
if DB_DEBUG == True :
    BROKER_URL = 'amqp://rabbituser:Aa123456@192.168.43.226:5672//'
else :
    BROKER_URL = 'amqp://rabbituser:Aa123456@192.168.43.226:5672//'
	 #BROKER_URL = 'amqp://rabbit:1@127.0.0.1:5672//'

CELERY_REDIRECT_STDOUTS_LEVEL='DEBUG'
CELERYD_HIJACK_ROOT_LOGGER = False

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json','pickle']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_ACKS_LATE = True
CELERYD_POOL_RESTARTS=True

#runs job synchronous
if ENVIRONMENT_DEV == True:
    BROKER_BACKEND='memory'
    CELERY_ALWAYS_EAGER  = True

#runs job synchronous
if ENVIRONMENT_DEV == True:
    BROKER_BACKEND='memory'
    CELERY_ALWAYS_EAGER  = True

from kombu import Queue,Exchange
CELERY_QUEUES = (
    Queue('default'     , Exchange('default')     , routing_key='printmanager.default'),        
    Queue('fileWatcher', Exchange('watcher'), routing_key='printmanager.watcher'), 
     Queue('generator', Exchange('generator'), routing_key='printmanager.generator'), 
)

CELERY_ROUTES = {     
    'jobs.tasks.runWatcher': {'queue': 'watcher', 'routing_key': 'printmanager.watcher'},
    'jobs.tasks.runGenerator': {'queue': 'generator', 'routing_key': 'printmanager.generator'}, 
    }

CELERYBEAT_SCHEDULE = {
    #===========================================================================
   
     'fileWatcher': {
         'task': 'jobs.tasks.runWatcher',
         'schedule': timedelta(minutes=5),
         'args': (),
     }                      
}
