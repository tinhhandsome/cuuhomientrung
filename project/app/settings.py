"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ
import sentry_sdk
import calendar
import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

env = environ.Env(
    DEBUG=(bool, True),
    DB_NAME=(str, 'cuuhomientrung'),
    DB_USER=(str, 'administrator'),
    DB_PASSWORD=(str, 'bangtin_ainews_2811#'),
    DB_HOSTNAME=(str, '103.192.236.67'),
    DB_PORT=(int, 5432),
    MAPBOX_KEY=(str, 'pk.eyJ1IjoiZHp1bmdkYSIsImEiOiJja2drMDFka2wwMW9zMndxZW9lMXBud3d5In0.oKlf9RF-X-SKkUJUAQ9ndw'),
    SENTRY_DSN=(str, None),
    DEPLOY_ENV=(str, 'local'),
    GIT_VERSION=(str, None),
    CSRF_COOKIE_SECURE=(bool, False),
)
env.read_env(
    os.path.join(BASE_DIR, '..', '.env')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ybcim6=@)la&g9@!asz1rx95=qd&39$tl1j1(1uflb_$mo*w##'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rangefilter',
    'django_admin_listfilter_dropdown',
    'django.contrib.sites',
    'rest_framework',
    'django_restful_admin',
    'smart_selects',
    'dynamic_raw_id',
    'admin_numeric_filter',
    'mapbox_location_field',
    'simple_history',
    'django_select2',
    'django_select2_admin_filters',
    'admin_auto_filters',
    'easy_select2',
    'webpack_loader',
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(name)s %(message)s [PID:%(process)d:%(threadName)s]"
            )
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            # 5 MB
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'filename': os.path.join(BASE_DIR, '..', 'logs', 'logs_errors.log'),
            'filters': ['require_debug_false'],
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            'filters': [],
        },
    },
    "loggers": {
        'django.request': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        "django": {
            "handlers": ["console", "errors_file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.server": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}


MAPBOX_KEY = env('MAPBOX_KEY')
DEPLOY_ENV = env('DEPLOY_ENV')
SENTRY_DSN = env('SENTRY_DSN')
GIT_VERSION = env('GIT_VERSION')
if SENTRY_DSN:
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    import logging

    integrations = [DjangoIntegration()]
    logger_level = logging.INFO
    sentry_logging = LoggingIntegration(
        level=logger_level,
        event_level=logger_level
    )
    integrations.append(sentry_logging)
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,
        send_default_pii=True,
        environment=DEPLOY_ENV,
        release=GIT_VERSION,
    )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'app.middleware.RestAPICsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'app.middleware.AutomaticUserLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]


ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'app.context_processors.global_params',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'
SITE_ID = 1

# USE THIS SETTING IF RUNNING ON LOCAL

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# USE THIS SETTING IF RUNNING ON PRODUCTION

DATABASES = {
        'default':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOSTNAME'),
        'PORT': env('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'deploy')

STATIC_URL = '/static/'

print(os.path.join(BASE_DIR, '..', 'static', 'webpack_bundles'))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static', 'webpack_bundles'),
)

MEDIA_ROOT = BASE_DIR + '/media'
MEDIA_URL = '/media/'

APPEND_SLASH = False

CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE')

X_FRAME_OPTIONS = 'SAMEORIGIN'

REVISION = calendar.timegm(time.gmtime())

SELECT2_USE_BUNDLED_JQUERY = False

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'webpack_bundles/', # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [],
        'EXCLUDE_RUNTIME': False,
        'BASE_ENTRYPOINT': ''
    }
}
